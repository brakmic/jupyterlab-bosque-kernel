from ipykernel.kernelbase import Kernel
from .wrapper import BosqueWrapper, BosqueExecutionError
import os
import tempfile
import shutil
import logging


class BosqueKernel(Kernel):
    """
    A custom Jupyter kernel for the Bosque programming language.
    """

    implementation = 'BosqueKernel'
    implementation_version = '1.0'
    language = 'bosque'
    language_version = '1.0'
    language_info = {
        'name': 'bosque',
        'version': '1.0',
        'mimetype': 'text/x-bosque',
        'file_extension': '.bsq',
        'pygments_lexer': 'bosque'
    }
    banner = "Bosque Language Kernel"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.connection_file = kwargs.get('connection_file', None)
        self.temp_dir = None

        try:
            self.bosque = BosqueWrapper()

            # Create a temporary directory for execution
            try:
                self.temp_dir = tempfile.mkdtemp(prefix='bosque_kernel_')
                logging.debug(f"Temporary directory created at {self.temp_dir}")
            except Exception as e:
                logging.error(f"Failed to create temporary directory: {e}")
                raise RuntimeError("Cannot create temporary directory.")

            # Log environment variables
            path = os.environ.get('PATH', '')
            logging.debug(f"Environment PATH: {path}")

            # Check if 'bosque' is accessible
            bosque_path = shutil.which('bosque')
            if not bosque_path:
                raise RuntimeError("'bosque' executable not found in PATH.")
            logging.debug(f"'bosque' executable found at: {bosque_path}")

            # Check if 'node' is accessible
            node_path = shutil.which('node')
            if not node_path:
                raise RuntimeError("'node' executable not found in PATH.")
            logging.debug(f"'node' executable found at: {node_path}")

        except Exception as e:
            logging.exception("Failed to initialize BosqueKernel")
            raise es

    def do_execute(self, code, silent=False, store_history=True,
                   user_expressions=None, allow_stdin=False):
        """
        Executes the Bosque code synchronously.

        :param code: The code to execute.
        :param silent: If True, do not send any output.
        :return: Execution result.
        """
        if not silent:
            # Signal that execution is starting
            self.send_response(self.iopub_socket, 'status', {'execution_state': 'busy'})
            logging.debug("Kernel is busy executing code.")

        try:
            # Change to the temporary directory
            original_cwd = os.getcwd()
            try:
                os.chdir(self.temp_dir)
                logging.debug(f"Changed working directory to {self.temp_dir}")
            except OSError as e:
                logging.error(f"Error changing working directory: {e}")
                raise RuntimeError("Failed to change working directory.")

            # Compile and execute Bosque code
            output = self._compile_and_execute(code)
            logging.debug("Code compiled and executed successfully.")

            if not silent:
                # Send the output to the frontend
                stream_content = {'name': 'stdout', 'text': output}
                self.send_response(self.iopub_socket, 'stream', stream_content)
                logging.debug("Output sent to frontend.")

            # Restore the original working directory
            os.chdir(original_cwd)
            logging.debug(f"Restored working directory to {original_cwd}")

            if not silent:
                self.send_response(self.iopub_socket, 'status', {'execution_state': 'idle'})
                logging.debug("Kernel status set to idle.")

            return {'status': 'ok',
                    'execution_count': self.execution_count,
                    'payload': [],
                    'user_expressions': {}}

        except BosqueExecutionError as e:
            # Send the error message to the frontend
            if not silent:
                self.send_error(e)
            logging.error(f"BosqueExecutionError: {e}")

            # Restore the original working directory
            os.chdir(original_cwd)
            logging.debug(f"Restored working directory to {original_cwd}")

            return {'status': 'error',
                    'execution_count': self.execution_count,
                    'ename': 'BosqueExecutionError',
                    'evalue': str(e),
                    'traceback': []}

        except Exception as e:
            # Handle unexpected exceptions
            if not silent:
                self.send_error(e)
            logging.error(f"Unexpected error: {e}", exc_info=True)

            # Restore the original working directory
            os.chdir(original_cwd)
            logging.debug(f"Restored working directory to {original_cwd}")

            return {'status': 'error',
                    'execution_count': self.execution_count,
                    'ename': type(e).__name__,
                    'evalue': str(e),
                    'traceback': []}

    def _compile_and_execute(self, code):
        """
        Compiles and executes Bosque code within the temporary directory.

        :param code: The Bosque code to execute.
        :return: The standard output from execution.
        :raises BosqueExecutionError: If compilation or execution fails.
        """
        try:
            logging.debug("Starting compilation and execution of Bosque code.")
            return self.bosque.compile_and_execute(code, work_dir=self.temp_dir)
        except Exception as e:
            logging.error(f"Error during Bosque execution: {e}")
            raise BosqueExecutionError(f"Execution failed: {str(e)}")
    def do_kernel_info_request(self, stream, ident, parent):
        content = {
            'status': 'ok',
            'protocol_version': '5.3',
            'implementation': self.implementation,
            'implementation_version': self.implementation_version,
            'language_info': self.language_info,
            'banner': self.banner,
        }
        self.session.send(stream, 'kernel_info_reply', content, parent, ident)

    def send_error(self, exception):
        """
        Sends an error message to the Jupyter frontend.

        :param exception: The exception to send.
        """
        ename = type(exception).__name__
        evalue = str(exception)
        traceback = []  # Optionally, include a traceback

        error_content = {
            'ename': ename,
            'evalue': evalue,
            'traceback': traceback
        }
        self.send_response(self.iopub_socket, 'error', error_content)
        logging.debug(f"Error sent to frontend: {ename} - {evalue}")

    def do_shutdown(self, restart):
        """
        Handles kernel shutdown.

        :param restart: Whether the kernel should restart.
        """
        # Clean up the temporary directory
        if self.temp_dir:
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            logging.debug(f"Temporary directory {self.temp_dir} removed.")
        super().do_shutdown(restart)

def main():
    import logging
    import sys

    # Configure logging to output to stderr
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        stream=sys.stderr
    )
    logging.debug("Launching BosqueKernel...")

    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=BosqueKernel)
    
if __name__ == "__main__":
    main()

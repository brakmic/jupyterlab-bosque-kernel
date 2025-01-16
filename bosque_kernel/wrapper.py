import subprocess
import os
from pathlib import Path

class BosqueExecutionError(Exception):
    """Custom exception for Bosque execution errors."""
    pass

class BosqueWrapper:
    """
    A wrapper to handle Bosque compilation and execution.
    Isolates Bosque-specific logic for easy maintenance and future extensions.
    """

    def __init__(self, bosque_command='bosque', node_command='node', main_js_filename='Main.mjs'):
        """
        Initialize the wrapper with commands to invoke Bosque and Node.js.

        :param bosque_command: Command to invoke the Bosque compiler.
        :param node_command: Command to invoke Node.js.
        :param main_js_filename: The expected main JavaScript file name after compilation.
        """
        self.bosque_command = bosque_command
        self.node_command = node_command
        self.main_js_filename = main_js_filename

    def compile_bosque(self, bosque_code, work_dir):
        """
        Compiles Bosque code to JavaScript using the Bosque compiler.

        :param bosque_code: A string containing Bosque code.
        :param work_dir: The working directory to execute commands in.
        :return: Path to the output directory containing generated JavaScript files.
        :raises BosqueExecutionError: If compilation fails.
        """
        # Determine the source file path
        source_file_path = os.path.join(work_dir, 'source.bsq')

        # Write the Bosque code to the source.bsq file
        with open(source_file_path, 'w') as source_file:
            source_file.write(bosque_code)

        # Determine the output directory (jsout in the same directory as source.bsq)
        output_dir = os.path.join(work_dir, 'jsout')
        os.makedirs(output_dir, exist_ok=True)

        # Compile Bosque code
        compile_proc = subprocess.run(
            [self.bosque_command, source_file_path],
            capture_output=True,
            text=True,
            cwd=work_dir
        )

        # Remove the source.bsq file after compilation
        os.remove(source_file_path)

        if compile_proc.returncode != 0:
            error_msg = compile_proc.stderr.strip() or 'Unknown compilation error.'
            raise BosqueExecutionError(f"Compilation failed: {error_msg}")

        if not os.path.isdir(output_dir):
            raise BosqueExecutionError(f"Compilation succeeded but output directory '{output_dir}' was not found.")

        return output_dir

    def find_main_js(self, output_dir):
        """
        Identifies the main JavaScript file to execute.

        :param output_dir: Directory containing generated JavaScript files.
        :return: Path to the main JavaScript file.
        :raises BosqueExecutionError: If the main JS file is not found.
        """
        main_js_path = os.path.join(output_dir, self.main_js_filename)
        if not os.path.isfile(main_js_path):
            # Attempt to find any .mjs or .js file as a fallback
            js_files = list(Path(output_dir).glob('*.mjs')) + list(Path(output_dir).glob('*.js'))
            if js_files:
                main_js_path = str(js_files[0])
            else:
                raise BosqueExecutionError(f"Main JavaScript file '{self.main_js_filename}' not found in '{output_dir}'.")

        return main_js_path

    def execute_js(self, js_path, work_dir):
        """
        Executes the generated JavaScript file using Node.js.

        :param js_path: Path to the JavaScript file.
        :param work_dir: The working directory to execute commands in.
        :return: The standard output from the execution.
        :raises BosqueExecutionError: If execution fails.
        """
        execute_proc = subprocess.run(
            [self.node_command, js_path],
            capture_output=True,
            text=True,
            cwd=work_dir
        )

        if execute_proc.returncode != 0:
            error_msg = execute_proc.stderr.strip() or 'Unknown execution error.'
            raise BosqueExecutionError(f"Execution failed: {error_msg}")

        return execute_proc.stdout

    def compile_and_execute(self, bosque_code, work_dir):
        """
        Compiles and executes Bosque code.

        :param bosque_code: The Bosque code to execute.
        :param work_dir: The working directory to execute commands in.
        :return: The standard output from execution.
        :raises BosqueExecutionError: If compilation or execution fails.
        """
        output_dir = self.compile_bosque(bosque_code, work_dir)
        main_js = self.find_main_js(output_dir)
        output = self.execute_js(main_js, work_dir)
        return output

    def compile_bosque_future(self, bosque_code, work_dir):
        """
        Future-proof method to compile Bosque code.
        Placeholder for future enhancements where Bosque might produce binaries.

        :param bosque_code: The Bosque code to compile.
        :param work_dir: The working directory to execute commands in.
        :return: Path to the executable or output.
        :raises BosqueExecutionError: If compilation fails.
        """
        # Placeholder method for future implementations
        raise NotImplementedError("Future compilation methods can be implemented here.")

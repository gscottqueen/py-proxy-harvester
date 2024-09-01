# Function to get the full path of a command
get_command_path() {
  command -v $1
}

## Set the root directory
ROOT_DIR=$(git rev-parse --show-toplevel)
CURRENT_DIR="${PWD##*/}"

echo "Current directory ${CURRENT_DIR}"

# Check if Python 3 is installed and install if not
PYTHON3_PATH=$(get_command_path python3)
if [ -z "$PYTHON3_PATH" ]; then
    echo "Python 3 is not installed. Attempting to install Python 3..."
    $(get_command_path brew) install python3 || { echo "Failed to install Python 3. Please install it manually."; exit 1; }
    PYTHON3_PATH=$(get_command_path python3)
fi

# Check if venv module is available in Python, install if not
if ! $PYTHON3_PATH -c "import venv" &> /dev/null; then
    echo "venv module is not available. Python installation might not support venv."
    exit 1
fi

# Set up Python virtual environment
if [ ! -d ".venv" ]; then
    $PYTHON3_PATH -m venv .venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi
source $ROOT_DIR/.venv/bin/activate

# Check if TruffleHog3 is installed and install if not
$(get_command_path pip) install -r requirements.txt --ignore-installed

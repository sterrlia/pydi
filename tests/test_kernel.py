from pathlib import Path
from pydi.kernel import DefaultKernel
from pydi.config import Config


root = str(Path(__file__).parent)
kernel = DefaultKernel(
    config=Config({}), 
    build_schemes=[], 
    project_dir=root, 
    index_dir="test_indexing"
)

kernel.boot()

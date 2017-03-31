from src import CommInterface
from src.ControladoresFiltros import Shutter

CommInterfaceVar, Motor = CommInterface.create_object()
print(dir(CommInterface))

CommInterface.Shutter.open_shutter()

#Shutter.open_shutter(CommInterfaceVar)

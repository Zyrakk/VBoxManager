import os

def listar_maquinas():

    # Guardamos el resultado del comando para listar maquinas en forma de texto
    listar_vm = 'vboxmanage list vms'

    proceso = os.popen(listar_vm)

    resultado = proceso.read()

    proceso.close()

    print()
    print("--- Lista de maquinas virtuales en el sistema ---")
    print(resultado)
    print()


def clonar_maquina():

    # Guardar parametros
    nombre = input("Introduce el nombre de la maquina que quieres clonar: ")
    nombre_nuevo = input("Introduce el nombre para la maquina clonada: ")

    # Ejecutat el comando y guardar la salida
    clonar_vm = f'vboxmanage clonevm {nombre} --name {nombre_nuevo} --register'

    salida = os.system(clonar_vm)

    # Verificaciones
    if salida == 0:
        print(f'La maquina {nombre} se ha clonado con exito.')
    else:
        print(f'La maquina {nombre} no se ha podido clonar.')


def iniciar_maquina():
    
    # Elegir interfaz de inicio
    nombre = input("Introduce el nombre de la maquina a iniciar: ")
    print()
    print("Modo de Inicio:")
    print("1. Con interfaz grafica.")
    print("2. Sin interfaz grafica.")
    opc = int(input("Elige una opcion [1,2]: "))
    
    match opc:
        case 1:
            iniciar = f'vboxmanage startvm "{nombre}"'
        case 2:
            iniciar = f'vboxmanage startvm "{nombre}" --type headless'
        case _:
            print()
            print("Debes introducir 1 o 2.")
            return
    
    # Guardar la salida del comando y verificar si se ejecuta correctamente
    salida = os.system(iniciar)
        
    if salida == 0:
        print(f'La maquina {nombre} se ha iniciado con exito.')
    else:
        print(f'La maquina {nombre} no se ha podido iniciar.')
    

def crear_maquina():
    
    # Guardar parametros
    nombre = input("Introduce el nombre de la maquina virtual: ")
    sistema_operativo = input("Introduce el tipo de sistema operativo (ej. Ubuntu_64, Windows10_64): ")
    ram = input("Introduce la cantidad de RAM en MB: ")
    size_disco = input("Introduce el tamaño para el disco en MB (20480 para 20G): ")
    ruta_iso = input("Introduce la ruta completa de la imagen ISO (ej. C:\\ruta\\archivo.iso): ")
    
    # Crear la maquina y configurarla
    crear_vm = f'vboxmanage createvm --name "{nombre}" --ostype {sistema_operativo} --register'
    config_vm = f'vboxmanage modifyvm "{nombre}" --memory {ram} --acpi on --boot1 dvd --nic1 nat'
    
    # Crear el disco virtual y conectarlo
    disco_virtual = (
        f'vboxmanage createmedium disk --filename "{nombre}.vdi" --size {size_disco} && '
        f'vboxmanage storagectl "{nombre}" --name "SATA Controller" --add sata --controller IntelAHCI && '
        f'vboxmanage storageattach "{nombre}" --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium "{nombre}.vdi'
    )
    
    # Crear un controlador IDE e instalar la imagen ISO
    ide_iso = (
        f'vboxmanage storagectl "{nombre}" --name "IDE Controller" --add ide && '
        f'vboxmanage storageattach "{nombre}" --storagectl "IDE Controller" --port 0 --device 0 --type dvddrive --medium "{ruta_iso}"'
    )
    
    # Verificaciones
    if (
        os.system(crear_vm) == 0 
        and os.system(config_vm) == 0
        and os.system(disco_virtual) == 0
        and os.system(ide_iso) == 0
    ):
        print()
        print("La máquina virtual se creó y configuró correctamente con los siguientes datos:")
        print(f'Nombre: {nombre}')
        print(f'SO: {sistema_operativo}')
        print(f'Ram: {ram}MB')
        print(f'Tamaño del disco: {size_disco}MB')
        print(f'Ruta de la imagen ISO: {ruta_iso}')
    else:
        print("Error al crear o configurar la máquina virtual.")


def borrar_maquina():

    # Guardar parametros
    nombre = input("Introduce el nombre de la maquina virtual que quieres borrar: ")

    # Comandos
    detener_vm = f'vboxmanage controlvm "{nombre}" poweroff >nul 2>&1'
    eliminar_vm = f'vboxmanage unregistervm "{nombre}" --delete >nul 2>&1'

    # Comprobar si existe la VM
    existe_vm = f'vboxmanage showvminfo "{nombre}" >nul 2>&1'

    salida_existe = os.system(existe_vm)

    if salida_existe != 0:
        print(f'La maquina {nombre} no existe o no se puede acceder a ella.')
        return
    
    # Borrar la VM
    salida_stop = os.system(detener_vm)
    
    if salida_stop != 0:
        print(f'La maquina {nombre} no se pudo detener, puede que ya este apagada.')
        
    salida_borrar = os.system(eliminar_vm)
    
    if salida_borrar == 0:
        print(f'La maquina {nombre} se elimino correctamente.')
    else:
        print(f'La maquina {nombre} no se pudo eliminar.')       


# Variables globales
    #
    #


def menu():

    # Comprobar que vboxmanage esta instalado y es accesible
    comprobacion_vbox = os.system("vboxmanage --version >nul 2>&1")
    
    if comprobacion_vbox != 0:
        print("VBoxManager no esta instalado o no es accesible.")
        return

    # Menu
    while True:
        print()
        print("------------- VirtualBox ---------------")
        print("1. Listar las maquinas instaladas.")
        print("2. Clonar una maquina virtual.")
        print("3. Iniciar una maquina.")
        print("4. Crear una maquina virtual.")
        print("5. Borrar una maquina virtual.")
        print("6. Salir.")
        print("------------------------------------")
        print()
        opc = int(input("Selecciona una opcion [1,2,3,4,5]: "))

        match opc:
            case 1:
                listar_maquinas()
            case 2:
                clonar_maquina()
            case 3:
                iniciar_maquina()
            case 4:
                crear_maquina()
            case 5:
                borrar_maquina()
            case 6:
                break
            case _:
                print("Introduce una opcion correcta: [1,2,3,4,5]")


if __name__ == "__main__":
    menu()
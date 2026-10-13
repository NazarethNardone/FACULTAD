from typing import List, Optional


class Estudiante:
    def __init__(self, matricula: str, nombre: str, apellido: str, carrera: str):
        self.__matricula = ""
        self.setMatricula(matricula)

        self.nombre = nombre
        self.apellido = apellido
        self.carrera = carrera

        self.cursos: List['Curso'] = []

    def agregarCurso(self, curso: 'Curso'):
        self.cursos.append(curso)

    def sacarCurso(self, curso: 'Curso'):
        if curso in self.cursos:
            self.cursos.remove(curso)

    def getMatricula(self) -> str:
        return self.__matricula

    def setMatricula(self, matricula: str):
        if matricula.isdigit() and len(matricula) >= 4 and len(matricula) <= 10:
            self.__matricula = matricula
        else:
            print("Matrícula inválida: debe contener solo dígitos y tener entre 4 y 10 caracteres.")

    def nombreCompleto(self) -> str:
        return self.nombre + " " + self.apellido


class Curso:
    def __init__(self, nombre: str, codigo: str, profesor: str, capacidad: int):
        self.nombre = nombre
        self.codigo = codigo
        self.profesor = profesor
        self.capacidad = capacidad

        self.inscriptos: List[Estudiante] = []

    def inscribir(self, estudiante: Estudiante):   # Inscripción a Cursos
        self.inscriptos.append(estudiante)

    def cuposDisponibles(self) -> int:  
        return self.capacidad - len(self.inscriptos)    #El sistema debe actualizar el número de estudiantes inscritos

    def darDeBaja(self, estudiante: Estudiante):
        if estudiante in self.inscriptos:
            self.inscriptos.remove(estudiante)


def pedir_texto(mensaje: str, campo: str) -> Optional[str]:
    texto = input(mensaje)
    if texto == "":
        print(campo, "inválido: no puede estar vacío.")
        return None
    for letra in texto:
        if letra.isdigit():
            print(campo, "inválido: no puede tener números.")
            return None
    return texto


def pedir_entero_positivo(mensaje: str) -> Optional[int]:
    try:
        numero = int(input(mensaje))
    except ValueError:
        print("Debe ingresar un número.")
        return None
    if numero <= 0:
        print("Debe ingresar un número mayor a cero.")
        return None
    return numero


class Facultad:
    def __init__(self):
        self.cursos: List[Curso] = []
        self.estudiantes: List[Estudiante] = []

    def buscarCurso(self, codigo: str) -> Optional[Curso]:
        for curso in self.cursos:
            if curso.codigo == codigo:
                return curso
        return None

    def buscarEstudiante(self, matricula: str) -> Optional[Estudiante]: 
        for estudiante in self.estudiantes:
            if estudiante.getMatricula() == matricula:
                return estudiante
        return None

    def altaCurso(self):
        codigo = input("Ingrese el código del curso: ")
        if codigo == "":
            print("El código no puede estar vacío.")
            return

        curso = self.buscarCurso(codigo)
        if curso:
            cupos_nuevos = pedir_entero_positivo("El curso ya existe. ¿Cuántos cupos desea agregar?: ")
            if cupos_nuevos is None:
                return
            curso.capacidad += cupos_nuevos
            print("Cupos agregados con éxito.")
        else:
            nombre = input("Ingrese el nombre del curso: ")
            if nombre == "":
                print("El nombre no puede estar vacío.")
                return
            profesor = pedir_texto("Ingrese el profesor encargado: ", "Profesor")
            if profesor is None:
                return
            capacidad = pedir_entero_positivo("Ingrese la capacidad máxima de estudiantes: ")
            if capacidad is None:
                return
            self.cursos.append(Curso(nombre, codigo, profesor, capacidad))
            print("Curso registrado con éxito.")

    def bajaCurso(self):   #Baja de Cursos
        codigo = input("Ingrese el código del curso a borrar: ")
        curso = self.buscarCurso(codigo)
        if not curso:
            print("El curso no existe.")
            return
        if len(curso.inscriptos) > 0:
            print("No se puede eliminar el curso: tiene estudiantes inscriptos.")
            return
        self.cursos.remove(curso)
        print("Curso eliminado.")

    def altaEstudiante(self):
        nombre = pedir_texto("Ingrese el nombre del estudiante: ", "Nombre")
        if nombre is None:
            return
        apellido = pedir_texto("Ingrese el apellido del estudiante: ", "Apellido")
        if apellido is None:
            return
        matricula = input("Ingrese el número de matrícula: ")

        if self.buscarEstudiante(matricula):
            print("Ya existe un estudiante registrado con esa matrícula.")
            return
        carrera = pedir_texto("Ingrese la carrera del estudiante: ", "Carrera")
        if carrera is None:
            return

        nuevo = Estudiante(matricula, nombre, apellido, carrera)
        if nuevo.getMatricula() != matricula:
            return
        self.estudiantes.append(nuevo)
        print("Estudiante registrado con éxito.")

    def bajaEstudiante(self):
        matricula = input("Ingrese la matrícula del estudiante a borrar: ")
        estudiante = self.buscarEstudiante(matricula)
        if not estudiante:
            print("El estudiante no existe.")
            return
        if len(estudiante.cursos) > 0:
            print("No se puede borrar el estudiante: tiene inscripciones activas.")
            return
        self.estudiantes.remove(estudiante)
        print("Estudiante eliminado.")

    def inscribir(self): # Inscripción a Cursos:
        matricula = input("Ingrese la matrícula del estudiante: ")
        estudiante = self.buscarEstudiante(matricula)
        if not estudiante:
            print("El estudiante no existe.")
            return
        codigo = input("Ingrese el código del curso: ")
        curso = self.buscarCurso(codigo)
        if not curso:
            print("El curso no existe.")
            return
        if estudiante in curso.inscriptos:
            print("El estudiante ya está inscripto en ese curso.")
            return
        if curso.cuposDisponibles() > 0:
            curso.inscribir(estudiante)
            estudiante.agregarCurso(curso)
            print("Estudiante inscripto exitosamente.")
        else:
            print("No hay cupos disponibles en este curso.")

    def bajaInscripcion(self):  # Baja de Cursos
        matricula = input("Ingrese la matrícula del estudiante: ")
        estudiante = self.buscarEstudiante(matricula)
        if not estudiante:
            print("El estudiante no existe.")
            return
        codigo = input("Ingrese el código del curso: ")
        curso = self.buscarCurso(codigo)
        if not curso:
            print("El curso no existe.")
            return
        if estudiante in curso.inscriptos:
            curso.darDeBaja(estudiante)
            estudiante.sacarCurso(curso)
            print("Baja del curso realizada exitosamente.")
        else:
            print("El estudiante no está inscripto en ese curso.")

    def listarCursos(self):  
        if not self.cursos:
            print("No hay cursos registrados.")
            return
        print("\n--- ESTADO DE LOS CURSOS ---")
        for c in self.cursos:
            print("Curso:", c.nombre, "| Código:", c.codigo, "| Profesor:", c.profesor,
                  "| Capacidad:", c.capacidad, "| Inscriptos:", len(c.inscriptos),
                  "| Cupos disponibles:", c.cuposDisponibles())

    def listarEstudiantes(self): #debe registrar qué estudiantes están inscritos en cada curso.
        if not self.estudiantes:
            print("No hay estudiantes registrados.")
            return
        print("\n--- ESTADO DE LOS ESTUDIANTES ---")
        for e in self.estudiantes:
            print("Estudiante:", e.nombreCompleto(), "Matrícula:", e.getMatricula(), "Carrera:", e.carrera)
            if e.cursos:
                for curso in e.cursos:
                    print("    -", curso.nombre, "(" + curso.codigo + ")")
            else:
                print("    Sin cursos inscriptos.")

    def listarCursosDeEstudiante(self):
        matricula = input("Ingrese la matrícula del estudiante: ")
        estudiante = self.buscarEstudiante(matricula)
        if not estudiante:
            print("El estudiante no existe.")
            return
        if not estudiante.cursos:
            print(estudiante.nombreCompleto(), "no está inscripto en ningún curso.")
            return
        print("\n--- CURSOS DE", estudiante.nombreCompleto(), "---")
        for curso in estudiante.cursos:
            print("Curso:", curso.nombre, "Código:", curso.codigo, "Profesor:", curso.profesor)


def menu() -> str:
    print("   Sistema de Gestión de Facultad")
    print("1- Agregar Curso")
    print("2- Quitar Curso")
    print("3- Agregar Estudiante")
    print("4- Borrar Estudiante")
    print("5- Inscribir Estudiante a Curso")
    print("6- Dar de Baja Inscripción")
    print("7- Mostrar Cursos")
    print("8- Mostrar Estudiantes")
    print("9- Mostrar Cursos de un Estudiante")
    print("10- Salir")
    return input("Seleccione una opción: ")


def main():
    facultad_urquiza = Facultad()

    while True:
        opcion = menu()
        if opcion == "10":
            break
        elif opcion == "1":
            facultad_urquiza.altaCurso()
        elif opcion == "2":
            facultad_urquiza.bajaCurso()
        elif opcion == "3":
            facultad_urquiza.altaEstudiante()
        elif opcion == "4":
            facultad_urquiza.bajaEstudiante()
        elif opcion == "5":
            facultad_urquiza.inscribir()
        elif opcion == "6":
            facultad_urquiza.bajaInscripcion()
        elif opcion == "7":
            facultad_urquiza.listarCursos()
        elif opcion == "8":
            facultad_urquiza.listarEstudiantes()
        elif opcion == "9":
            facultad_urquiza.listarCursosDeEstudiante()
        else:
            print("Opción no válida, intente de nuevo.")
    print("\nPrograma Terminado.")


if __name__ == "__main__":
    main()
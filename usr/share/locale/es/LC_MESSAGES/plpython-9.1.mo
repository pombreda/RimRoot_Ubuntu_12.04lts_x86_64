��    J      l  e   �      P     Q     T  )   o  Z   �     �  =        Q  >   i  )   �  )   �  /   �  A   ,  M   n  K   �  9   	  3   B	  (   v	     �	     �	  <   �	  $   
  ?   4
     t
  r   �
  b     i   h  .   �  4     &   6  )   ]  0   �  0   �  h   �  6   R     �     �  @   �       7     (   U     ~  +   �  !   �  "   �          %  *   B  '   m  &   �  ;   �  J   �  L   C     �  B   �     �  '     4   8  -   m  >   �  H   �  "   #  2   F  '   y  ,   �  +   �  (   �  0   #  .   T  2   �  $   �  !   �     �       �  5     �     �  0     x   @  '   �  B   �     $  ?   >  3   ~  5   �  0   �  Q     `   k  b   �  G   /  A   w  <   �     �       J   )  2   t  G   �     �  u     i   �     �  0   n  ?   �  ,   �  0     0   =  8   n  u   �  @        ^  %   |  Z   �      �  K     ,   j     �  3   �  "   �  +   
   '   6   #   ^   4   �   4   �   2   �   2   !  T   R!  J   �!  ,   �!  W   "     w"  *   �"  7   �"  (   �"  C   ##  W   g#  %   �#  ;   �#  +   !$  (   M$  '   v$  (   �$  F   �$  >   %  1   M%  4   %  (   �%  &   �%  ,   &            ,   1      7                 B       *   
      +   4   2   9            0           E       >   !          /   F                  ;   #   5   J   <             G   	   (      "   6                 D                     A   %   3   ?           '          C                 $         I   &             :   .       )   -              @   8             =       H       %s Expected None or a string. Expected None, "OK", "SKIP", or "MODIFY". Expected sequence of %d argument, got %d: %s Expected sequence of %d arguments, got %d: %s PL/Python anonymous code block PL/Python does not support conversion to arrays of row types. PL/Python function "%s" PL/Python function with return type "void" did not return None PL/Python functions cannot accept type %s PL/Python functions cannot return type %s PL/Python only supports one-dimensional arrays. PL/Python set-returning functions must return an iterable object. PL/Python set-returning functions only support returning only value per call. PL/Python trigger function returned "MODIFY" in a DELETE trigger -- ignored PyDict_SetItemString() failed, while setting up arguments PyList_SetItem() failed, while setting up arguments Python major version mismatch in session SPI_execute failed: %s SPI_execute_plan failed: %s Start a new session to use a different Python major version. TD["new"] deleted, cannot modify row TD["new"] dictionary key at ordinal position %d is not a string TD["new"] is not a dictionary This session has previously used Python major version %d, and it is now attempting to use Python major version %d. To return null in a column, add the value None to the mapping with the key named after the column. To return null in a column, let the returned object have an attribute named after column with value None. attribute "%s" does not exist in Python object cannot convert multidimensional array to Python list could not add the spiexceptions module could not compile PL/Python function "%s" could not compile anonymous PL/Python code block could not convert Python Unicode object to bytes could not convert Python object into cstring: Python string representation appears to contain null bytes could not create bytes representation of Python object could not create globals could not create new dictionary could not create new dictionary while building trigger arguments could not create new list could not create string representation of Python object could not create the base SPI exceptions could not execute plan could not extract bytes from encoded string could not generate SPI exceptions could not import "__main__" module could not import "plpy" module could not initialize globals could not parse error message in plpy.elog could not unpack arguments in plpy.elog error fetching next item from iterator forcibly aborting a subtransaction that has not been exited function returning record called in context that cannot accept type record key "%s" found in TD["new"] does not exist as a column in the triggering row key "%s" not found in mapping length of returned sequence did not match number of columns in row plan.status takes no arguments plpy.execute expected a query or a plan plpy.execute takes a sequence as its second argument plpy.prepare does not support composite types plpy.prepare: type name at ordinal position %d is not a string return value of function with array return type is not a Python sequence returned object cannot be iterated second argument of plpy.prepare must be a sequence there is no subtransaction to exit from this subtransaction has already been entered this subtransaction has already been exited this subtransaction has not been entered trigger functions can only be called as triggers unexpected return value from trigger procedure unrecognized error in PLy_spi_execute_fetch_result unsupported set function return mode untrapped error in initialization while creating return value while modifying trigger row Project-Id-Version: plpython (PostgreSQL 9.1)
Report-Msgid-Bugs-To: pgsql-bugs@postgresql.org
POT-Creation-Date: 2013-01-29 13:50+0000
PO-Revision-Date: 2012-02-21 22:54-0300
Last-Translator: Alvaro Herrera <alvherre@alvh.no-ip.org>
Language-Team: PgSQL-es-Ayuda <pgsql-es-ayuda@postgresql.org>
Language: es
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=2; plural=n != 1;
 %s Se esperaba None o una cadena. Se esperaba None, «OK», «SKIP» o «MODIFY». Se esperaba una secuencia de %d argumento, se obtuvo %d: %s Se esperaba una secuencia de %d argumentos, se obtuvo %d: %s bloque de código anónimo de PL/Python PL/Python no soporta la conversión de arrays a tipos de registro. función PL/Python «%s» función PL/Python con tipo de retorno «void» no retorna None la funciones PL/Python no pueden aceptar el tipo %s las funciones PL/Python no pueden retornar el tipo %s PL/Python sólo soporta arrays unidimensionales. Los funciones PL/Python que retornan conjuntos deben retornar un objeto iterable. Las funciones PL/Python que retornan conjuntos sólo permiten retornar un valor por invocación. función de disparador de PL/Python retorno «MODIFY» en un disparador de tipo DELETE -- ignorado PyDict_SetItemString() falló, mientras se inicializaban los argumentos PyList_SetItem() falló, mientras se inicializaban los argumentos las versiones mayores de Python no coinciden en esta sesión falló SPI_execute: %s falló SPI_execute_plan: %s Inicie una nueva sesión para usar una versión mayor de Python diferente. TD["new"] borrado, no se puede modicar el registro el nombre del atributo de TD["new"] en la posición %d no es una cadena TD["new"] no es un diccionario Esta sesión ha usado previamente la versión mayor de Python %d, y ahora está intentando usar la versión mayor %d. Para retornar null en una columna, agregue el valor None al mapa, con llave llamada igual que la columna. Para retornar null en una columna, haga que el objeto retornado tenga un atributo llamado igual que la columna, con valor None. el atributo «%s» no existe en el objeto Python no se puede convertir array multidimensional a una lista Python no se pudo importar el módulo spiexceptions no se pudo compilar la función PL/Python «%s» no se pudo compilar el bloque anónimo PL/Python no se pudo convertir el objeto Unicode de Python a bytes no se pudo convertir el objeto Python a un cstring: la representación de cadena Python parece tener bytes nulos (\0) no se pudo crear la representación de cadena de bytes de Python no se pudo crear las globales no se pudo crear un nuevo diccionario no se pudo crear un nuevo diccionario mientras se construían los argumentos de disparador no se pudo crear una nueva lista no se pudo crear la representación de cadena de texto del objeto de Python no se pudo crear las excepciones SPI basales no se pudo ejecutar el plan no se pudo extraer bytes desde la cadena codificada no se pudo generar excepciones SPI no se pudo importar el módulo «__main__» no se pudo importar el módulo «plpy» no se pudo inicializar las globales no se pudo analizar el mensaje de error de plpy.elog no se pudo desempaquetar los argumentos de plpy.elog error extrayendo el próximo elemento del iterador abortando una subtransacción que no se ha cerrado se llamó una función que retorna un registro en un contexto que no puede aceptarlo la llave «%s» en TD["new"] no existe como columna en la fila disparadora la llave «%s» no fue encontrada en el mapa el tamaño de la secuencia retornada no concuerda con el número de columnas de la fila plan.status no lleva argumentos plpy.execute espera una consulta o un plan plpy.execute lleva una secuencia como segundo argumento plpy.prepare no soporta tipos compuestos plpy.prepare: el nombre de tipo en la posición %d no es una cadena el valor de retorno de la función con tipo de retorno array no es una secuencia Python objeto retornado no puede ser iterado el segundo argumento de plpy.prepare debe ser una secuencia no hay una subtransacción de la cual salir ya se ha entrado en esta subtransacción ya se ha salido de esta subtransacción no se ha entrado en esta subtransacción las funciones disparadoras sólo pueden ser llamadas como disparadores valor de retorno no esperado desde el procedimiento disparador error desconocido en PLy_spi_execute_fetch_result modo de retorno de conjunto de función no soportado error no capturado en la inicialización mientras se creaba el valor de retorno mientras se modificaba la fila de disparador 
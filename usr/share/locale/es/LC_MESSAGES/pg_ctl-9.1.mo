��    �      T  �   �      `  D   a  ?   �  I   �      0     Q  &   c     �     �  -   �     �       =         ^     {  �   �     (  a   H  K   �     �  A     !   S  3   u  ?   �  ?   �  H   )  D   r  C   �  E   �  ?   A  >   �  9   �  B   �  <   =  �   z  0   �  F   0  >   w  8   �  I   �  %   9  2   _  O   �  7   �          !     *  M   <  -   �  !   �  >   �  E     C   _  y   �  9     D   W  C   �  D   �  >   %  A   d  !   �  2   �  +   �  *   '  /   R  %   �  &   �  /   �  #   �     #  3   A  2   u  1   �  0   �  ,     .   8  3   g  -   �  0   �  5   �  :   0  1   k  *   �  "   �  $   �  J        [     w  3   �  0   �     �       !   %  $   G      l  -   �  4   �  %   �  $     "   ;  !   ^  F   �  u   �  F   =      �   7   �   )   �   k   �   `   f!  %   �!  &   �!     "  d   "     �"  &   �"  0   �"  .   �"  )   '#  )   Q#  "   {#      �#  (   �#     �#  !   $     %$     9$     V$     h$     ~$     �$     �$     �$     �$  "   �$     �$  �  %  L   �&  R   �&  R   H'  +   �'     �'  (   �'  "   (  &   '(  0   N(     (  #   �(  @   �(  )   �(     ))  �   I)     �)  h   �)  M   _*     �*  C   �*     +  4   ++  E   `+  I   �+  r   �+  y   c,  v   �,  ~   T-  O   �-  k   #.  9   �.  F   �.  H   /  �   Y/  5   �/  L   (0  H   u0  L   �0  K   1  ,   W1  8   �1  k   �1  J   )2     t2     |2     �2  Y   �2  8   �2  '   03  H   X3  h   �3  T   
4  �   _4  O   �4  f   H5  f   �5  g   6  [   ~6  e   �6  &   @7  C   g7  /   �7  .   �7  0   
8  2   ;8  .   n8  =   �8  ,   �8  &   9  A   /9  F   q9  =   �9  /   �9  2   &:  2   Y:  F   �:  A   �:  ?   ;  C   U;  G   �;  F   �;  ,   (<  /   U<  /   �<  Q   �<  !   =  "   )=  ;   L=  A   �=     �=     �=  /   �=  +   .>  -   Z>  D   �>  G   �>  ,   ?  )   B?  *   l?  (   �?  P   �?  �   @  D   �@  #   �@  A   A  )   DA  w   nA  u   �A  5   \B  2   �B     �B  �   �B  '   VC  1   ~C  5   �C  5   �C  /   D  /   LD  )   |D  ,   �D  /   �D  !   E  +   %E     QE     mE     �E     �E  %   �E     �E     �E     F  '   F  '   BF  &   jF     l   f       K   )   H   j   r              �   B   7   ]      z         I      �   _   s       u          �   /   (   P   Q   1   m   J           +      3   o              q   w   D   ;   E   6   &      T   !   }   <   4   C       '                         h         
       ~       �                      y   e   @   b   ?       �      a               �             U       	          `   ,   t   Y      5              g       *      >       L               d   "       A   �   V   %   8              v   .   $   R       F   k   S   #   M   ^   i             -   [   Z   \      W       :   O   2       x   9   �         X   |      N   p       n                  0   =   c       G       {    
%s: -w option cannot use a relative socket directory specification
 
%s: -w option is not supported when starting a pre-9.1 server
 
%s: this data directory appears to be running a pre-existing postmaster
 
Allowed signal names for kill:
 
Common options:
 
Options for register and unregister:
 
Options for start or restart:
 
Options for stop or restart:
 
Report bugs to <pgsql-bugs@postgresql.org>.
 
Shutdown modes are:
 
Start types are:
   %s init[db]               [-D DATADIR] [-s] [-o "OPTIONS"]
   %s kill    SIGNALNAME PID
   %s promote [-D DATADIR] [-s]
   %s register   [-N SERVICENAME] [-U USERNAME] [-P PASSWORD] [-D DATADIR]
                    [-S START-TYPE] [-w] [-t SECS] [-o "OPTIONS"]
   %s reload  [-D DATADIR] [-s]
   %s restart [-w] [-t SECS] [-D DATADIR] [-s] [-m SHUTDOWN-MODE]
                 [-o "OPTIONS"]
   %s start   [-w] [-t SECS] [-D DATADIR] [-s] [-l FILENAME] [-o "OPTIONS"]
   %s status  [-D DATADIR]
   %s stop    [-W] [-t SECS] [-D DATADIR] [-s] [-m SHUTDOWN-MODE]
   %s unregister [-N SERVICENAME]
   --help                 show this help, then exit
   --version              output version information, then exit
   -D, --pgdata DATADIR   location of the database storage area
   -N SERVICENAME  service name with which to register PostgreSQL server
   -P PASSWORD     password of account to register PostgreSQL server
   -S START-TYPE   service start type to register PostgreSQL server
   -U USERNAME     user name of account to register PostgreSQL server
   -W                     do not wait until operation completes
   -c, --core-files       allow postgres to produce core files
   -c, --core-files       not applicable on this platform
   -l, --log FILENAME     write (or append) server log to FILENAME
   -m SHUTDOWN-MODE   can be "smart", "fast", or "immediate"
   -o OPTIONS             command line options to pass to postgres
                         (PostgreSQL server executable) or initdb
   -p PATH-TO-POSTGRES    normally not necessary
   -s, --silent           only print errors, no informational messages
   -t SECS                seconds to wait when using -w option
   -w                     wait until operation completes
   auto       start service automatically during system startup (default)
   demand     start service on demand
   fast        quit directly, with proper shutdown
   immediate   quit without complete shutdown; will lead to recovery on restart
   smart       quit after all clients have disconnected
  done
  failed
  stopped waiting
 %s is a utility to initialize, start, stop, or control a PostgreSQL server.

 %s: -S option not supported on this platform
 %s: PID file "%s" does not exist
 %s: WARNING: cannot create restricted tokens on this platform
 %s: WARNING: could not locate all job object functions in system API
 %s: another server might be running; trying to start server anyway
 %s: cannot be run as root
Please log in (using, e.g., "su") as the (unprivileged) user that will
own the server process.
 %s: cannot promote server; server is not in standby mode
 %s: cannot promote server; single-user server is running (PID: %ld)
 %s: cannot reload server; single-user server is running (PID: %ld)
 %s: cannot restart server; single-user server is running (PID: %ld)
 %s: cannot set core file size limit; disallowed by hard limit
 %s: cannot stop server; single-user server is running (PID: %ld)
 %s: could not allocate SIDs: %lu
 %s: could not create promote signal file "%s": %s
 %s: could not create restricted token: %lu
 %s: could not find own program executable
 %s: could not find postgres program executable
 %s: could not open PID file "%s": %s
 %s: could not open process token: %lu
 %s: could not open service "%s": error code %d
 %s: could not open service manager
 %s: could not read file "%s"
 %s: could not register service "%s": error code %d
 %s: could not remove promote signal file "%s": %s
 %s: could not send promote signal (PID: %ld): %s
 %s: could not send reload signal (PID: %ld): %s
 %s: could not send signal %d (PID: %ld): %s
 %s: could not send stop signal (PID: %ld): %s
 %s: could not start server
Examine the log output.
 %s: could not start server: exit code was %d
 %s: could not start service "%s": error code %d
 %s: could not unregister service "%s": error code %d
 %s: could not wait for server because of misconfiguration
 %s: could not write promote signal file "%s": %s
 %s: database system initialization failed
 %s: invalid data in PID file "%s"
 %s: missing arguments for kill mode
 %s: no database directory specified and environment variable PGDATA unset
 %s: no operation specified
 %s: no server running
 %s: old server process (PID: %ld) seems to be gone
 %s: option file "%s" must have exactly one line
 %s: out of memory
 %s: server does not shut down
 %s: server is running (PID: %ld)
 %s: service "%s" already registered
 %s: service "%s" not registered
 %s: single-user server is running (PID: %ld)
 %s: too many command-line arguments (first is "%s")
 %s: unrecognized operation mode "%s"
 %s: unrecognized shutdown mode "%s"
 %s: unrecognized signal name "%s"
 %s: unrecognized start type "%s"
 (The default is to wait for shutdown, but not for start or restart.)

 HINT: The "-m fast" option immediately disconnects sessions rather than
waiting for session-initiated disconnection.
 If the -D option is omitted, the environment variable PGDATA is used.
 Is server running?
 Please terminate the single-user server and try again.
 Server started and accepting connections
 The program "%s" is needed by %s but was not found in the
same directory as "%s".
Check your installation.
 The program "%s" was found by "%s"
but was not the same version as %s.
Check your installation.
 Timed out waiting for server startup
 Try "%s --help" for more information.
 Usage:
 WARNING: online backup mode is active
Shutdown will not complete until pg_stop_backup() is called.

 Waiting for server startup...
 child process exited with exit code %d child process exited with unrecognized status %d child process was terminated by exception 0x%X child process was terminated by signal %d child process was terminated by signal %s could not change directory to "%s" could not find a "%s" to execute could not identify current directory: %s could not read binary "%s" could not read symbolic link "%s" invalid binary "%s" server is still starting up
 server promoting
 server shutting down
 server signaled
 server started
 server starting
 server stopped
 starting server anyway
 waiting for server to shut down... waiting for server to start... Project-Id-Version: pg_ctl (PostgreSQL 9.1)
Report-Msgid-Bugs-To: pgsql-bugs@postgresql.org
POT-Creation-Date: 2013-01-29 13:56+0000
PO-Revision-Date: 2012-02-21 22:53-0300
Last-Translator: Álvaro Herrera <alvherre@alvh.no-ip.org>
Language-Team: PgSQL Español <pgsql-es-ayuda@postgresql.org>
Language: es
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
 
%s: la opción -w no puede usar una especificación relativa de directorio
 
%s: la opción -w no está soportada cuando se inicia un servidor anterior a 9.1
 
%s: este directorio de datos parece estar ejecutando un postmaster pre-existente
 
Nombres de señales permitidos para kill:
 
Opciones comunes:
 
Opciones para registrar y dar de baja:
 
Opciones para inicio y reinicio:
 
Opciones para detención y reinicio:
 
Reporte errores a <pgsql-bugs@postgresql.org>.
 
Modos de detención son:
 
Tipos de inicio del servicio son:
   %s init[db]               [-D DATADIR] [-s] [-o «OPCIONES»]
   %s kill    NOMBRE-SEÑAL ID-DE-PROCESO
   %s promote [-D DATADIR] [-s]
   %s register   [-N SERVICIO] [-U USUARIO] [-P PASSWORD] [-D DATADIR]
                    [-S TIPO-INICIO] [-w] [-t SEGS] [-o «OPCIONES»]
   %s reload  [-D DATADIR] [-s]
   %s restart [-w] [-t SEGS] [-D DATADIR] [-s] [-m MODO-DETENCIÓN]
                   [-o «OPCIONES»]
   %s start   [-w] [-t SEGS] [-D DATADIR] [-s] [-l ARCHIVO] [-o «OPCIONES»]
   %s status  [-D DATADIR]
   %s stop    [-W] [-t SEGS] [-D DATADIR] [-s] [-m MODO-DETENCIÓN]
   %s unregister [-N SERVICIO]
   --help                 mostrar este texto y salir
   --version              mostrar información sobre versión y salir
   -D, --pgdata DATADIR   ubicación del área de almacenamiento de datos
   -N SERVICIO            nombre de servicio con el cual registrar
                         el servidor PostgreSQL
   -P CONTRASEÑA          contraseña de la cuenta con la cual registrar
                         el servidor PostgreSQL
   -S TIPO-INICIO         tipo de inicio de servicio con que registrar
                         el servidor PostgreSQL
   -U USUARIO             nombre de usuario de la cuenta con la cual
                         registrar el servidor PostgreSQL
   -W                     no esperar hasta que la operación se haya completado
   -c, --core-files       permite que postgres produzca archivos
                         de volcado (core)
   -c, --core-files       no aplicable en esta plataforma
   -l  --log ARCHIVO      guardar el registro del servidor en ARCHIVO.
   -m MODO-DE-DETENCIÓN   puede ser «smart», «fast» o «immediate»
   -o OPCIONES            parámetros de línea de órdenes a pasar a postgres
                         (ejecutable del servidor de PostgreSQL) o initdb
   -p RUTA-A-POSTGRES     normalmente no es necesario
   -s, --silent           mostrar sólo errores, no mensajes de información
   -t SEGS                segundos a esperar cuando se use la opción -w
   -w                     esperar hasta que la operación se haya completado
   auto       iniciar automáticamente al inicio del sistema (por omisión)
   demand     iniciar el servicio en demanda
   fast        salir directamente, con apagado apropiado
   immediate   salir sin apagado completo; se ejecutará recuperación
              en el próximo inicio

   smart       salir después que todos los clientes se hayan desconectado
  listo
  falló
  abandonando la espera
 %s es un programa para inicializar, iniciar, detener o controlar un servidor PostgreSQL.
 %s: la opción -S no está soportada en esta plataforma
 %s: el archivo de PID «%s» no existe
 %s: ATENCIÓN: no se pueden crear tokens restrigidos en esta plataforma
 %s: ATENCIÓN: no fue posible encontrar todas las funciones de gestión de tareas en la API del sistema
 %s: otro servidor puede estar en ejecución; tratando de iniciarlo de todas formas.
 %s: no puede ser ejecutado como root
Por favor conéctese (por ej. usando «su») con un usuario no privilegiado,
quien ejecutará el proceso servidor.
 %s: no se puede promover el servidor;
el servidor no está en modo «standby»
 %s: no se puede promover el servidor;
un servidor en modo mono-usuario está en ejecución (PID: %ld)
 %s: no se puede recargar el servidor;
un servidor en modo mono-usuario está en ejecución (PID: %ld)
 %s: no se puede reiniciar el servidor;
un servidor en modo mono-usuario está en ejecución (PID: %ld)
 %s: no se puede establecer el límite de archivos de volcado;
impedido por un límite duro
 %s: no se puede detener el servidor;
un servidor en modo mono-usuario está en ejecución (PID: %ld)
 %s: no se pudo emplazar los SIDs: %lu
 %s: no se pudo crear el archivo de señal de promoción «%s»: %s
 %s: no se pudo crear el token restringido: %lu
 %s: no se pudo encontrar el propio ejecutable
 %s: no se pudo encontrar el ejecutable postgres
 %s: no se pudo abrir el archivo de PID «%s»: %s
 %s: no se pudo abrir el token de proceso: %lu
 %s: no se pudo abrir el servicio «%s»: código de error %d
 %s: no se pudo abrir el gestor de servicios
 %s: no se pudo leer el archivo «%s»
 %s: no se pudo registrar el servicio «%s»: código de error %d
 %s: no se pudo eliminar el archivo de señal de promoción «%s»: %s
 %s: no se pudo enviar la señal de promoción (PID: %ld): %s
 %s: la señal de recarga falló (PID: %ld): %s
 %s: no se pudo enviar la señal %d (PID: %ld): %s
 %s: falló la señal de detención (PID: %ld): %s
 %s: no se pudo iniciar el servidor.
Examine el registro del servidor.
 %s: no se pudo iniciar el servidor: el código de retorno fue %d
 %s: no se pudo iniciar el servicio «%s»: código de error %d
 %s: no se pudo dar de baja el servicio «%s»: código de error %d
 %s: no se pudo esperar al servidor debido a un error de configuración
 %s: no se pudo escribir al archivo de señal de promoción «%s»: %s
 %s: falló la creación de la base de datos
 %s: datos no válidos en archivo de PID «%s»
 %s: argumentos faltantes para envío de señal
 %s: no se especificó directorio de datos y la variable PGDATA no está definida
 %s: no se especificó operación
 %s: no hay servidor en ejecución
 %s: el proceso servidor antiguo (PID: %ld) parece no estar
 %s: archivo de opciones «%s» debe tener exactamente una línea
 %s: memoria agotada
 %s: el servidor no se detiene
 %s: el servidor está en ejecución (PID: %ld)
 %s: el servicio «%s» ya está registrado
 %s: el servicio «%s» no ha sido registrado
 %s: un servidor en modo mono-usuario está en ejecución (PID: %ld)
 %s: demasiados argumentos de línea de órdenes (el primero es «%s»)
 %s: modo de operación «%s» no reconocido
 %s: modo de apagado «%s» no reconocido
 %s: nombre de señal «%s» no reconocido
 %s: tipo de inicio «%s» no reconocido
 (Por omisión se espera para las detenciones, pero no los inicios o reinicios)

 SUGERENCIA: La opción «-m fast» desconecta las sesiones inmediatamente
en lugar de esperar que cada sesión finalice por sí misma.
 Si la opción -D es omitida, se usa la variable de ambiente PGDATA.
 ¿Está el servidor en ejecución?
 Por favor termine el servidor mono-usuario e intente nuevamente.
 Servidor iniciado y aceptando conexiones
 %s necesita el programa «%s», pero no pudo encontrarlo en el mismo
directorio que «%s».
Verifique su instalación.
 El programa «%s» fue encontrado por «%s», pero no es
de la misma versión que «%s».
Verifique su instalación.
 Se agotó el tiempo de espera al inicio del servidor
 Use «%s --help» para obtener más información.
 Empleo:
 ATENCIÓN: el modo de respaldo en línea está activo
El apagado no se completará hasta que se invoque la función pg_stop_backup().

 Esperando que el servidor se inicie...
 el proceso hijo terminó con código de salida %d el proceso hijo terminó con código no reconocido %d el proceso hijo fue terminado por una excepción 0x%X el proceso hijo fue terminado por una señal %d el proceso hijo fue terminado por una señal %s no se pudo cambiar el directorio a «%s» no se pudo encontrar un «%s» para ejecutar no se pudo identificar el directorio actual: %s no se pudo leer el binario «%s» no se pudo leer el enlace simbólico «%s» el binario %s no es válida servidor aún iniciándose
 servidor promoviendo
 servidor deteniéndose
 se ha enviado una señal al servidor
 servidor iniciado
 servidor iniciándose
 servidor detenido
 iniciando el servidor de todas maneras
 esperando que el servidor se detenga... esperando que el servidor se inicie... 
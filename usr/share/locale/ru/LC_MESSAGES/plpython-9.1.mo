��    J      l  e   �      P     Q     T  )   o  Z   �     �  =        Q  >   i  )   �  )   �  /   �  A   ,  M   n  K   �  9   	  3   B	  (   v	     �	     �	  <   �	  $   
  ?   4
     t
  r   �
  b     i   h  .   �  4     &   6  )   ]  0   �  0   �  h   �  6   R     �     �  @   �       7     (   U     ~  +   �  !   �  "   �          %  *   B  '   m  &   �  ;   �  J   �  L   C     �  B   �     �  '     4   8  -   m  >   �  H   �  "   #  2   F  '   y  ,   �  +   �  (   �  0   #  .   T  2   �  $   �  !   �     �         5     G  ,   J  6   w  G  �  .   �  h   %     �  [   �  E     G   N  T   �  �   �  �   �  |   ;  U   �  O     K   ^     �  $   �  �   �  S   q  p   �     6  �   V  �     �   �  F   ~   b   �   ?   (!  N   h!  _   �!  X   "  �   p"  d   '#  D   �#  1   �#  o   $  /   s$  f   �$  Y   
%  (   d%  X   �%  G   �%  F   .&  B   u&  V   �&  X   '  J   h'  ]   �'  g   (  �   y(  �   )  =   �)  �   �)  6   g*  8   �*  z   �*  F   R+  l   �+  �   ,  T   �,  i   �,  O   f-  5   �-  ;   �-  :   (.  f   c.  `   �.  I   +/  �   u/  K   �/  C   C0  :   �0            ,   1      7                 B       *   
      +   4   2   9            0           E       >   !          /   F                  ;   #   5   J   <             G   	   (      "   6                 D                     A   %   3   ?           '          C                 $         I   &             :   .       )   -              @   8             =       H       %s Expected None or a string. Expected None, "OK", "SKIP", or "MODIFY". Expected sequence of %d argument, got %d: %s Expected sequence of %d arguments, got %d: %s PL/Python anonymous code block PL/Python does not support conversion to arrays of row types. PL/Python function "%s" PL/Python function with return type "void" did not return None PL/Python functions cannot accept type %s PL/Python functions cannot return type %s PL/Python only supports one-dimensional arrays. PL/Python set-returning functions must return an iterable object. PL/Python set-returning functions only support returning only value per call. PL/Python trigger function returned "MODIFY" in a DELETE trigger -- ignored PyDict_SetItemString() failed, while setting up arguments PyList_SetItem() failed, while setting up arguments Python major version mismatch in session SPI_execute failed: %s SPI_execute_plan failed: %s Start a new session to use a different Python major version. TD["new"] deleted, cannot modify row TD["new"] dictionary key at ordinal position %d is not a string TD["new"] is not a dictionary This session has previously used Python major version %d, and it is now attempting to use Python major version %d. To return null in a column, add the value None to the mapping with the key named after the column. To return null in a column, let the returned object have an attribute named after column with value None. attribute "%s" does not exist in Python object cannot convert multidimensional array to Python list could not add the spiexceptions module could not compile PL/Python function "%s" could not compile anonymous PL/Python code block could not convert Python Unicode object to bytes could not convert Python object into cstring: Python string representation appears to contain null bytes could not create bytes representation of Python object could not create globals could not create new dictionary could not create new dictionary while building trigger arguments could not create new list could not create string representation of Python object could not create the base SPI exceptions could not execute plan could not extract bytes from encoded string could not generate SPI exceptions could not import "__main__" module could not import "plpy" module could not initialize globals could not parse error message in plpy.elog could not unpack arguments in plpy.elog error fetching next item from iterator forcibly aborting a subtransaction that has not been exited function returning record called in context that cannot accept type record key "%s" found in TD["new"] does not exist as a column in the triggering row key "%s" not found in mapping length of returned sequence did not match number of columns in row plan.status takes no arguments plpy.execute expected a query or a plan plpy.execute takes a sequence as its second argument plpy.prepare does not support composite types plpy.prepare: type name at ordinal position %d is not a string return value of function with array return type is not a Python sequence returned object cannot be iterated second argument of plpy.prepare must be a sequence there is no subtransaction to exit from this subtransaction has already been entered this subtransaction has already been exited this subtransaction has not been entered trigger functions can only be called as triggers unexpected return value from trigger procedure unrecognized error in PLy_spi_execute_fetch_result unsupported set function return mode untrapped error in initialization while creating return value while modifying trigger row Project-Id-Version: PostgreSQL 9.1
Report-Msgid-Bugs-To: pgsql-bugs@postgresql.org
POT-Creation-Date: 2012-08-06 11:51+0000
PO-Revision-Date: 2012-08-06 17:37+0400
Last-Translator: Alexander Lakhin <exclusion@gmail.com>
Language-Team: Russian <pgtranslation-translators@pgfoundry.org>
Language: ru
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=3; plural=n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2;
X-Generator: Lokalize 1.4
 %s Ожидалось None или строка. Ожидалось None, "OK", "SKIP" или "MODIFY". Ожидалась последовательность из %d аргумента, получено %d: %s Ожидалась последовательность из %d аргументов, получено %d: %s Ожидалась последовательность из %d аргументов, получено %d: %s анонимный блок кода PL/Python PL/Python не поддерживает преобразование в массивы кортежей. функция PL/Python "%s" функция PL/Python с типом результата "void" вернула не None функции PL/Python не могут принимать тип %s функции PL/Python не могут возвращать тип %s PL/Python поддерживает только одномерные массивы. Функции PL/Python с результатом-множеством должны возвращать объекты с возможностью итерации. Функции PL/Python с результатом-множеством могут возвращать только по одному значению за вызов. триггерная функция PL/Python вернула "MODIFY" в триггере DELETE -- игнорируется ошибка в PyDict_SetItemString() при настройке аргументов ошибка в PyList_SetItem() при настройке аргументов несовпадение базовой версии Python в сеансе ошибка в SPI_execute: %s ошибка в SPI_execute_plan: %s Чтобы переключиться на другую базовую версию Python, начните новый сеанс. элемент TD["new"] удалён -- изменить строку нельзя ключ словаря TD["new"] с порядковым номером %d не является строкой TD["new"] - не словарь В данном сеансе до этого использовался Python базовой версии %d, а сейчас планируется использовать Python версии %d. Чтобы присвоить колонке NULL, добавьте в сопоставление значение None с ключом-именем колонки. Чтобы присвоить колонке NULL, присвойте возвращаемому значению атрибут с именем колонки и значением None. в объекте Python не существует атрибут "%s" преобразовать многомерный массив в список Python нельзя не удалось добавить модуль spiexceptions не удалось скомпилировать функцию PL/Python "%s" не удалось скомпилировать анонимный блок кода PL/Python не удалось преобразовать объект Python Unicode в байты не удалось преобразовать объект Python в cstring: похоже, представление строки Python содержит нулевые байты не удалось создать байтовое представление объекта Python не удалось создать глобальные данные не удалось создать словарь не удалось создать словарь для передачи аргументов триггера не удалось создать список не удалось создать строковое представление объекта Python не удалось создать базовые объекты исключений SPI нельзя выполнить план не удалось извлечь байты из кодированной строки не удалось сгенерировать исключения SPI не удалось импортировать модуль "__main__" не удалось импортировать модуль "plpy" не удалось инициализировать глобальные данные не удалось разобрать сообщение об ошибке в plpy.elog не удалось распаковать аргументы в plpy.elog ошибка получения следующего элемента из итератора принудительное прерывание незавершённой подтранзакции функция, возвращающая запись, вызвана в контексте, не допускающем этот тип ключу "%s", найденному в TD["new"], не соответствует колонка в строке, обрабатываемой триггером ключ "%s" не найден в сопоставлении длина возвращённой последовательности не равна числу колонок в строке plan.status не принимает аргументы plpy.execute ожидает запрос или план plpy.execute принимает в качестве второго аргумента последовательность plpy.prepare не поддерживает составные типы plpy.prepare: имя типа с порядковым номером %d не является строкой возвращаемое значение функции с результатом-массивом не является последовательностью возвращаемый объект не поддерживает итерации вторым аргументом plpy.prepare должна быть последовательность нет подтранзакции, которую нужно закончить эта подтранзакция уже начата эта подтранзакция уже закончена эта подтранзакция ещё не начата триггерные функции могут вызываться только в триггерах триггерная процедура вернула недопустимое значение нераспознанная ошибка в PLy_spi_execute_fetch_result неподдерживаемый режим возврата для функции с результатом-множеством необработанная ошибка при инициализации при создании возвращаемого значения при изменении строки в триггере 
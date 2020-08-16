---
title: Python 变量命名规范
tags: ["Python"]
key: Python 变量命名规范
---
由 Python 之父推荐的[命名规范](https://www.python.org/dev/peps/pep-0008/#naming-conventions)

|Type|Public|Internal|
| ------ | ------ | ------ |
|Modules|lower_with_under|_lower_with_under|
|Packages|lower_with_under|
|Classes|CapWords|_CapWords|
|Exceptions|CapWords|
|Functions|lower_with_under()|_lower_with_under()|
|Global/Class Constants|CAPS_WITH_UNDER|_CAPS_WITH_UNDER|
|Global/Class Variables|lower_with_under|_lower_with_under|
|Instance Variables|lower_with_under|_lower_with_under (protected) or __lower_with_under (private)|
|Method Names|lower_with_under()|_lower_with_under() (protected) or __lower_with_under() (private)|
|Function/Method Parameters|lower_with_under|
|Local Variables|lower_with_under|

<!--more-->
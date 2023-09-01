from ctypes import *
import libcalc2
import sys

def die(msg):
    print(msg)
    exit(1)

if __name__ == '__main__':
    while True:
        print("> ", end='')
        try:
            s = input()
        except EOFError:
            sys.exit(0)

        expr = libcalc2.expr_type()
        if (libcalc2.calc_parse(s.encode('utf-8'), byref(expr)) != 0):
            die("unable to parse expression")

        simplified = libcalc2.expr_type()

        if (len(sys.argv) == 2 and sys.argv[1] == 'remove-zeros'):
            libcalc2.calc_remove_zeros(expr, byref(simplified))
        else:
            libcalc2.calc_simplify(expr, byref(simplified))

        result = c_char_p()
        if (libcalc2.calc_expression_to_string(simplified, byref(result)) != 0):
            die("unable to print expression to string")

        print('')
        print(result.value.decode('utf-8'))
        print('')

        libcalc2.lisp_release_handle(expr)
        libcalc2.lisp_release_handle(simplified)


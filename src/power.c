
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdbool.h>
#include <gmp.h>


int my_pow(const mpz_t base, const mpz_t exp, mpz_t result) {
    mpz_pow_ui(result, base, mpz_get_ui(exp));
    
    if (result == NULL) {
        return -1;
    }
    return 0;
}
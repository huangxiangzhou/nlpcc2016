#include <Python.h>

wchar_t *lcommon(const wchar_t *string1, const wchar_t *string2) {
	int strlen1 = wcslen(string1);
	int strlen2 = wcslen(string2);
	int i, j, end=0;
	int longest = 0;
	int **ptr = (int **)malloc((strlen1 + 1) * sizeof(int *));
    wchar_t *res;

	for (i = 0; i < strlen1 + 1; i++)
		ptr[i] = (int *)calloc((strlen2 + 1), sizeof(int));

	for (i = 1; i < strlen1 + 1; i++) {
		for (j = 1; j < strlen2 + 1; j++) {
			if (string1[i-1] == string2[j-1]) {
				ptr[i][j] = ptr[i-1][j-1] + 1;
                if (ptr[i][j] > longest) {
                    longest = ptr[i][j];
                    end = i;
                }
            }
            else {
				ptr[i][j] = 0;
			}
		}
	}
	for (i = 0; i < strlen1 + 1; i++)
		free(ptr[i]);
	free(ptr);
    
    res = (wchar_t *)calloc((longest + 1), sizeof(wchar_t));
    
	wcsncpy(res, &(string1[end-longest]), longest);
    //printf("substring from %d, length is %d\n", end-longest, longest);
	return res;
}

static PyObject * lcs_function(PyObject *self, PyObject *args) {
    const wchar_t *_a, *_b;
    wchar_t *ret = NULL;
    int strlen, i;
    if (!PyArg_ParseTuple(args, "uu", &_a, &_b))
        return NULL;

    //printf("input string1 is %ls\n", _a);
    //printf("input string2 is %ls\n", _b);
    ret = lcommon(_a, _b);

    return Py_BuildValue("u", ret); 
}

static PyMethodDef lcsMethods[] = {
    {
         "lcs",
         lcs_function,
         METH_VARARGS,
         ""
    },
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef lcs = {
    PyModuleDef_HEAD_INIT,
    "lcs",
    NULL,
    -1,
    lcsMethods
};

PyMODINIT_FUNC PyInit_lcs(void)
{
    PyObject *m;
    m = PyModule_Create(&lcs);
    if (m == NULL)
        return NULL;
    printf("init lcs module\n");
    return m;
}
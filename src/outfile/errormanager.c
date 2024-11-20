/*!
* \file errormanager.c
* \brief Source providing a simple interface for managing runtime error messages.
* \author Michael E. Tryby (US EPA - ORD/NRMRL)
* \date Created On: 2017-08-25
* \date Last Edited: 2024-10-17
*/
#include <string.h>
#include <stdlib.h>
#include "errormanager.h"


/*!
* \brief Constructs a new error handle.
* \param message_lookup Function pointer for error message lookup
* \return Pointer to instance of error manager handlke
*/
error_handle_t* new_error_manager(p_msg_lookup message_lookup)
{	
	error_handle_t *error_handle = NULL;
	error_handle = (error_handle_t*)calloc(1, sizeof(error_handle_t));

	error_handle->message_lookup = message_lookup;

	return error_handle;
}

/*!
* \brief Destroy error manager handle
* \param error_handle Pointer to error manager handle
*/
void dst_error_manager(error_handle_t* error_handle)
{
	free(error_handle);
}

/*!
* \brief Sets an error code in the handle.
* \param error_handle Pointer to error manager handle
* \param errorcode Error code
*/
int set_error(error_handle_t* error_handle, int errorcode)
{
	// If the error code is 0 no action is taken and 0 is returned.
	// This is a feature not a bug.
	if (errorcode)
		error_handle->error_status = errorcode;

	return errorcode;
}

/*!
* \brief Returns the error message or NULL.
* \param error_handle Pointer to error manager handle
* \return Error message or NULL
* \note Caller must free memory allocated by check_error
*/
char* check_error(error_handle_t* error_handle)
{
	char* temp = NULL;

	if (error_handle->error_status != 0) {
		temp = (char*) calloc(ERR_MAXMSG, sizeof(char));

		if (temp)
			error_handle->message_lookup(error_handle->error_status, temp, ERR_MAXMSG);
	}
	return temp;
}


/*!
* \brief Clears the error from the handle.
* \param error_handle Pointer to error manager handle
*/
void clear_error(error_handle_t* error_handle)
{
	error_handle->error_status = 0;
}

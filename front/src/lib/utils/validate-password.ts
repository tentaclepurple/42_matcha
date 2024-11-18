/**
 * Validates a password based on the following criteria:
 * - Must be at least 8 characters long
 * - Must contain at least one lowercase letter
 * - Must contain at least one uppercase letter
 * - Must contain at least one number
 * - Must contain at least one special character
 *
 * @param password - The password string to validate.
 * @returns An object containing:
 * - `isValid`: A boolean indicating if the password is valid.
 * - `message`: A string message indicating the validation result.
 */
const validatePassword = (
	password: string
): {
	isValid: boolean;
	message: string;
} => {
	if (password.length < 8) {
		return {
			isValid: false,
			message: 'Password must be at least 8 characters long'
		};
	}

	if (!/[a-z]/.test(password)) {
		return {
			isValid: false,
			message: 'Password must contain a lowercase letter'
		};
	}

	if (!/[A-Z]/.test(password)) {
		console.log('mierda');
		return {
			isValid: false,
			message: 'Password must contain an uppercase letter'
		};
	}

	if (!/[0-9]/.test(password)) {
		return {
			isValid: false,
			message: 'Password must contain a number'
		};
	}

	if (!/[!@#$%^&*(),.?\":{}|<>]/.test(password)) {
		return {
			isValid: false,
			message: 'Password must contain a special character'
		};
	}

	return {
		isValid: true,
		message: ''
	};
};

export default validatePassword;

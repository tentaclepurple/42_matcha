/**
 * Calculates the date of the eighteenth birthday from today's date.
 *
 * @returns {string} The ISO string representation of the date 18 years ago from today, in the format 'YYYY-MM-DD'.
 */
export default function calcEighteenthBirthday(): string {
	const today = new Date();
	const eighteenYearsAgo = new Date(today.getFullYear() - 18, today.getMonth(), today.getDate());

	return eighteenYearsAgo.toISOString().split('T')[0];
}

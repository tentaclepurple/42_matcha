export default function serialize(obj: any): any {
	if (Array.isArray(obj)) {
		return obj.map((v) => serialize(v));
	} else if (typeof obj === 'object' && obj !== null) {
		return Object.keys(obj).reduce((result, key) => {
			const newKey = key === 'id' ? '_id' : key.replace(/[A-Z]/g, (m) => `_${m.toLowerCase()}`);
			return { ...result, [newKey]: serialize(obj[key]) };
		}, {});
	}
	return obj;
}

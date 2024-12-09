export default function deserialize(obj: object) {
	if (Array.isArray(obj)) {
		return obj.map((v) => deserialize(v));
	} else if (typeof obj === 'object' && obj !== null) {
		return Object.keys(obj).reduce((result, key) => {
			const newKey = key.replace(/_([a-z])/g, (m) => m[1].toUpperCase());
			return { ...result, [newKey]: deserialize(obj[key]) };
		}, {});
	}
	return obj;
}
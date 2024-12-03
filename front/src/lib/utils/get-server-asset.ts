import { SERVER_BASE_URL } from '$lib/constants/api';

/**
 * Retrieves the URL for a server asset.
 *
 * @param assetName - The name of the asset to retrieve.
 * @returns The full URL to the asset on the server.
 */
export default function getServerAsset(assetName: string): string {
	if (assetName.startsWith('http')) {
		return assetName;
	}

	// Some asset come prefixed by 'app'
	if (assetName.startsWith('app') || assetName.startsWith('/app')) {
		const relativeAssetName = assetName.split('/').slice(1).join('/');
		return `${SERVER_BASE_URL}/${relativeAssetName}`;
	}

	return `${SERVER_BASE_URL}/${assetName}`;
}

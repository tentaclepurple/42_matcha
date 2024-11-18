/**
 * Retrieves the URL for a server asset.
 *
 * @param assetName - The name of the asset to retrieve.
 * @returns The full URL to the asset on the server.
 */
export default function getServerAsset(assetName: string): string {
	return `http://localhost:5000/${assetName}`;
}

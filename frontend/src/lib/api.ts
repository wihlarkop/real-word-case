import type { Challenge, CategoryOption } from './types';

const BASE_URL = 'http://localhost:8000/api/v1';

export async function fetchCategories(): Promise<{
	industries: CategoryOption[];
	roles: CategoryOption[];
	difficulties: CategoryOption[];
}> {
	const response = await fetch(`${BASE_URL}/category`);
	if (!response.ok) {
		throw new Error(`HTTP error! status: ${response.status}`);
	}
	return await response.json();
}

export async function generateChallenge(
	industry: string,
	role: string,
	difficulty: string
): Promise<string> {
	const response = await fetch(`${BASE_URL}/challenge`, {
		method: 'POST',
		headers: {
			accept: 'application/json',
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ industry, role, difficulty })
	});

	if (!response.ok) {
		let errorMsg = 'Something went wrong. ';
		try {
			const errData = await response.json();
			if (errData && errData.detail) {
				errorMsg += errData.detail;
			} else if (errData && errData.message) {
				errorMsg += errData.message;
			} else {
				errorMsg += `Server responded with status ${response.status}`;
			}
		} catch (e) {
			errorMsg += `Server responded with status ${response.status}`;
		}
		throw new Error(errorMsg);
	}

	const data = await response.json();
	return data.result;
}

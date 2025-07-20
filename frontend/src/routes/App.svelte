<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import Header from '$lib/components/Header.svelte';
	import WarningBanner from '$lib/components/WarningBanner.svelte';
	import Footer from '$lib/components/Footer.svelte';
	import ChallengeCard from '$lib/components/ChallengeCard.svelte';
	import DropdownGroup from '$lib/components/DropdownGroup.svelte';
	import Toast from '$lib/components/Toast.svelte';
	import CustomMarkdown from '$lib/components/CustomMarkdown.svelte';
	import type { Challenge, CategoryOption } from '$lib/types';
	import { fetchCategories, generateChallenge as apiGenerateChallenge } from '$lib/api';

	let categories = $state({
		industries: [] as CategoryOption[],
		roles: [] as CategoryOption[],
		difficulties: [] as CategoryOption[]
	});

	let selectedCategory = $state({
		industry: '',
		role: '',
		difficulty: ''
	});

	let challenges = $state([] as Challenge[]);
	let isGenerating = $state(false);
	let showWarningBanner = $state(false);
	let showExpandedView = $state(false);
	let expandedChallenge = $state(null as Challenge | null);
	let showToast = $state(false);
	let toastType = $state('copy');
	let toastChallengeTitle = $state('');
	let isCategoryError = $state(false);

	// Prevent accidental navigation away
	function handleBeforeUnload(event: BeforeUnloadEvent) {
		if (isGenerating) {
			event.preventDefault();
			event.returnValue = '';
			return '';
		}
	}

	onMount(async () => {
		if (typeof window !== 'undefined') {
			window.addEventListener('beforeunload', handleBeforeUnload);
		}
		try {
			const data = await fetchCategories();
			categories.industries = data.industries;
			categories.roles = data.roles;
			categories.difficulties = data.difficulties;
		} catch (error) {
			console.error('Failed to load categories:', error);
			isCategoryError = true;
		}
	});
	onDestroy(() => {
		if (typeof window !== 'undefined') {
			window.removeEventListener('beforeunload', handleBeforeUnload);
		}
	});


	function canSubmit(): boolean {
		return !isCategoryError &&
			categories.industries.length > 0 &&
			categories.roles.length > 0 &&
			categories.difficulties.length > 0 &&
			selectedCategory.industry !== '' &&
			selectedCategory.role !== '' &&
			selectedCategory.difficulty !== '';
	}

	async function generateChallenge(): Promise<void> {
		if (isGenerating) return;
		isGenerating = true;
		let challengeText: string = '';
		try {
			const { industry, role, difficulty } = selectedCategory;
			challengeText = await apiGenerateChallenge(industry, role, difficulty);
			showWarningBanner = false;
			const newChallenge: Challenge = {
				id: Date.now(),
				text: challengeText,
				industry: categories.industries.find((opt) => opt.value === industry)?.label || '',
				role: categories.roles.find((opt) => opt.value === role)?.label || '',
				difficulty: categories.difficulties.find((opt) => opt.value === difficulty)?.label || '',
				date: new Date().toLocaleDateString('en-US', {
					day: 'numeric',
					month: 'short',
					year: 'numeric'
				})
			};
			challenges = [newChallenge, ...challenges];
		} catch (error) {
			challengeText = error instanceof Error ? error.message : 'An unknown error occurred.';
			showWarningBanner = true;
		} finally {
			isGenerating = false;
		}
	}

	function deleteChallenge(id: number): void {
		challenges = challenges.filter((challenge) => challenge.id !== id);
	}

	function copyChallenge(challenge: Challenge): void {
		navigator.clipboard.writeText(challenge.text);
		const title = challenge.text.split(' ').slice(0, 3).join(' ') + '...';
		toastType = 'copy';
		toastChallengeTitle = title;
		showToast = true;
	}

	function shareChallenge(challenge: Challenge): void {
		const title = challenge.text.split(' ').slice(0, 3).join(' ') + '...';
		toastType = 'share';
		toastChallengeTitle = title;
		showToast = true;
	}

	function openChallengeInNewTab(challengeId: number): void {
		const challengeUrl = `${window.location.origin}/challenge/${challengeId}`;
		window.open(challengeUrl, '_blank');
	}

	function clearHistory(): void {
		challenges = [];
	}
</script>

<div class="min-h-screen bg-gray-50">
	<!-- Header -->
	<Header />

	<!-- Warning Banner -->
	<WarningBanner show={showWarningBanner} onClose={() => showWarningBanner = false} />

	<main class="max-w-4xl mx-auto px-6 py-8">
		<!-- Challenge Card: Show latest challenge at the top if exists -->
		{#if challenges.length > 0}
			<ChallengeCard
				challenge={challenges[0]}
				onExpand={() => { expandedChallenge = challenges[0]; showExpandedView = true; }}
				onCopy={() => copyChallenge(challenges[0])}
				onShare={() => shareChallenge(challenges[0])}
				onRegenerate={generateChallenge}
			/>
		{/if}

		<!-- Always show generate section below challenge card -->
		<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-8 mb-8 flex flex-col items-center">
			<div class="flex flex-col items-center mb-6">
				<!-- Directly render SVG, do NOT use slot or {@render} -->
				<svg class="w-14 h-14 text-gray-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 48 48">
					<circle cx="24" cy="24" r="22" stroke-width="4" class="opacity-10" />
					<path d="M24 14v10l7 7" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
				</svg>
				<h3 class="text-lg font-semibold text-gray-900 mb-1">Generate a New Challenge</h3>
				<p class="text-gray-500 text-sm">Pick a combination and generate your software engineering prompt.</p>
			</div>
			<DropdownGroup {categories} {selectedCategory} />
			<button
				onclick={generateChallenge}
				class="mt-6 inline-flex items-center justify-center px-6 py-3 text-base font-medium rounded-md text-white bg-red-500 hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition disabled:opacity-50"
				disabled={!canSubmit() || isGenerating}
			>
				{#if isGenerating}
					<div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
					Generating, please wait...
				{:else}
					Generate Challenge
				{/if}
			</button>
		</div>

		<!-- History Section: Always show all challenges, including latest -->
		<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-8 mb-8 mt-8">
			<div class="flex items-center justify-between mb-4">
				<div class="flex items-center gap-2">
					<svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path d="M3 12a9 9 0 1 0 9-9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
						<path d="M3 3v6h6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
					</svg>
					<span class="font-semibold text-lg text-gray-800">History</span>
					{#if challenges.length > 0}
						<span class="ml-2 bg-gray-100 text-gray-600 text-xs px-2 py-0.5 rounded-full">{challenges.length}</span>
					{/if}
				</div>
				<button class="text-gray-400 hover:text-red-500 flex items-center gap-1 text-sm font-medium"
								onclick={clearHistory} disabled={challenges.length === 0}>
					<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6h18" />
						<path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" stroke-width="2" />
						<path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m5 6v6m4-6v6" stroke-width="2" />
					</svg>
					Clear
				</button>
			</div>
			{#if challenges.length === 0}
				<div class="flex flex-col items-center justify-center py-12">
					<svg class="w-12 h-12 text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 48 48">
						<circle cx="24" cy="24" r="22" stroke-width="4" class="opacity-10" />
						<path d="M32 32c-2 2-8 2-10 0-2-2-2-8 0-10 2-2 8-2 10 0 2 2 2 8 0 10z" stroke-width="3"
									stroke-linecap="round" stroke-linejoin="round" />
						<path d="M28 36l2 2m-10-2l-2 2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
					</svg>
					<div class="font-medium text-gray-500 mb-1">No challenges generated yet</div>
					<div class="text-gray-400 text-sm">Your challenge history will appear here after you generate some
						challenges
					</div>
				</div>
			{:else}
				<div>
					{#each challenges as challenge, i}
						<ChallengeCard
							challenge={challenge}
							onExpand={() => { expandedChallenge = challenge; showExpandedView = true; }}
							onCopy={() => copyChallenge(challenge)}
							onShare={() => shareChallenge(challenge)}
							onRegenerate={i === 0 ? generateChallenge : null}
							onDelete={i !== 0 ? () => deleteChallenge(challenge.id) : null}
						/>
					{/each}
				</div>
			{/if}
		</div>
	</main>

	<!-- Footer -->
	<Footer />

	<!-- Expanded Challenge View -->
	{#if showExpandedView && expandedChallenge}
		<div class="fixed inset-0 bg-gray-50 z-50 flex items-center justify-center p-8">
			<div class="max-w-4xl mx-auto text-center">
				<button
					onclick={() => showExpandedView = false}
					class="absolute top-8 right-8 text-gray-400 hover:text-gray-600"
					aria-label="Close Expanded View"
				>
					<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
					</svg>
				</button>
				{#if typeof window !== 'undefined'}
					<CustomMarkdown
						content={expandedChallenge.text}
						variant="expanded"
					/>
				{/if}
			</div>
		</div>
	{/if}

	<!-- Toast Component -->
	<Toast
		bind:show={showToast}
		type={toastType}
		challengeTitle={toastChallengeTitle}
		onOpenNewTab={() => {
            const currentChallenge = challenges.find(c => c.text.includes(toastChallengeTitle.replace('...', '')));
            if (currentChallenge) {
                openChallengeInNewTab(currentChallenge.id);
            }
        }}
	/>
</div>

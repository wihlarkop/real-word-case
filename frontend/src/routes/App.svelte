<script>
    import {onMount, onDestroy} from 'svelte';
    import {browser} from '$app/environment';
    import Header from '$lib/components/Header.svelte';
    import WarningBanner from '$lib/components/WarningBanner.svelte';
    import Footer from '$lib/components/Footer.svelte';
    import ChallengeCard from '$lib/components/ChallengeCard.svelte';
    import DropdownGroup from '$lib/components/DropdownGroup.svelte';
    import Toast from '$lib/components/Toast.svelte';
    import CustomMarkdown from "$lib/components/CustomMarkdown.svelte";
    import {Clock} from 'lucide-svelte';

    // State using Svelte 5 runes
    let categories = $state({
        industries: [],
        roles: [],
        difficulties: []
    });

    let selectedCategory = $state({
        industry: '',
        role: '',
        difficulty: ''
    });

    let challenges = $state([]);
    let isLoading = $state(false);
    let isGenerating = $state(false);
    let showWarningBanner = $state(false);

    let showExpandedView = $state(false);
    let expandedChallenge = $state(null);

    // Toast state
    let showToast = $state(false);
    let toastType = $state('copy');
    let toastChallengeTitle = $state('');

    let isCategoryError = $state(false);

    let isLeaving = false;

    // Prevent accidental navigation away
    function handleBeforeUnload(event) {
        if (isGenerating) {
            event.preventDefault();
            event.returnValue = '';
            return '';
        }
    }

    onMount(() => {
        if (typeof window !== 'undefined') {
            window.addEventListener('beforeunload', handleBeforeUnload);
        }
    });
    onDestroy(() => {
        if (typeof window !== 'undefined') {
            window.removeEventListener('beforeunload', handleBeforeUnload);
        }
    });

    // Fetch categories from API
    async function fetchCategories() {
        try {
            const response = await fetch('http://localhost:8000/api/v1/category');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            // Use backend categories directly, do not add or hardcode 'Any ...' in FE
            categories.industries = data.industries || [];
            categories.roles = data.roles || [];
            categories.difficulties = data.difficulties || [];
        } catch (error) {
            console.error('Failed to fetch categories:', error);
            categories.industries = [];
            categories.roles = [];
            categories.difficulties = [];
            selectedCategory.industry = '';
            selectedCategory.role = '';
            selectedCategory.difficulty = '';
            isCategoryError = true;
        }
    }

    function canSubmit() {
        // All dropdowns must have a value (not empty string)
        return !isCategoryError &&
            categories.industries.length > 0 &&
            categories.roles.length > 0 &&
            categories.difficulties.length > 0 &&
            selectedCategory.industry !== '' &&
            selectedCategory.role !== '' &&
            selectedCategory.difficulty !== '';
    }

    // Generate challenge
    async function generateChallenge() {
        if (isGenerating) return; // Prevent double submit
        isGenerating = true;
        try {
            const industry = selectedCategory.industry;
            const role = selectedCategory.role;
            const difficulty = selectedCategory.difficulty;
            const response = await fetch('http://localhost:8000/api/v1/challenge', {
                method: 'POST',
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    industry,
                    role,
                    difficulty
                })
            });
            let challengeText = '';
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
                challengeText = errorMsg;
                showWarningBanner = true;
            } else {
                const data = await response.json();
                challengeText = data.result;
                showWarningBanner = false;
            }
            const newChallenge = {
                id: Date.now(),
                text: challengeText,
                industry: categories.industries.find(opt => opt.value === industry)?.label || '',
                role: categories.roles.find(opt => opt.value === role)?.label || '',
                difficulty: categories.difficulties.find(opt => opt.value === difficulty)?.label || '',
                date: new Date().toLocaleDateString('en-US', {
                    day: 'numeric',
                    month: 'short',
                    year: 'numeric',
                }),
            };
            challenges = [newChallenge, ...challenges];
        } catch (error) {
            const newChallenge = {
                id: Date.now(),
                text: 'That might happen, and we admit that!',
                industry: '',
                role: '',
                difficulty: '',
                date: new Date().toLocaleDateString('en-US', {
                    day: 'numeric',
                    month: 'short',
                    year: 'numeric',
                }),
            };
            challenges = [newChallenge, ...challenges];
            showWarningBanner = true;
        } finally {
            isGenerating = false;
        }
    }

    function deleteChallenge(id) {
        challenges = challenges.filter(challenge => challenge.id !== id);
    }

    function copyChallenge(challenge) {
        navigator.clipboard.writeText(challenge.text);

        // Extract challenge title from text (first few words)
        const title = challenge.text.split(' ').slice(0, 3).join(' ') + '...';

        // Show copy toast
        toastType = 'copy';
        toastChallengeTitle = title;
        showToast = true;
    }

    function shareChallenge(challenge) {
        // Generate a shareable URL (simulate)
        const challengeUrl = `${window.location.origin}/challenge/${challenge.id}`;
        navigator.clipboard.writeText(challengeUrl);

        // Extract challenge title from text (first few words)
        const title = challenge.text.split(' ').slice(0, 3).join(' ') + '...';

        // Show share toast
        toastType = 'share';
        toastChallengeTitle = title;
        showToast = true;
    }

    function openChallengeInNewTab(challengeId) {
        const challengeUrl = `${window.location.origin}/challenge/${challengeId}`;
        window.open(challengeUrl, '_blank');
    }

    function clearHistory() {
        challenges = [];
    }

    // Load categories on mount
    onMount(() => {
        fetchCategories();
    });
</script>

<div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <Header />

    <!-- Warning Banner -->
    <WarningBanner show={showWarningBanner} onClose={() => showWarningBanner = false} />

    <main class="max-w-4xl mx-auto px-6 py-8">
        {#if challenges.length > 0}
            <!-- Latest Challenge Display -->
            <ChallengeCard
                challenge={challenges[0]}
                isLatest={true}
                onExpand={() => { expandedChallenge = challenges[0]; showExpandedView = true; }}
                onCopy={() => copyChallenge(challenges[0])}
                onShare={() => shareChallenge(challenges[0])}
                onRegenerate={generateChallenge}
            />
        {/if}

        <!-- Dropdowns and Generate Button -->
        {#if challenges.length === 0}
            <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-8 mb-8">
                <div class="text-center mb-8">
                    <p class="text-gray-600 text-lg">
                        Sharpen your software engineering skills with open-ended, real-world prompts.
                    </p>
                </div>
                <DropdownGroup {categories} {selectedCategory} />
                <div class="text-center">
                    <button
                        onclick={generateChallenge}
                        disabled={isGenerating || !canSubmit()}
                        class="bg-red-500 hover:bg-red-600 disabled:bg-red-300 text-white px-8 py-3 rounded-lg font-medium transition-colors flex items-center gap-2 mx-auto"
                    >
                        {#if isGenerating}
                            <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                            Generating, please wait...
                        {:else}
                            Create New Challenge
                        {/if}
                    </button>
                </div>
            </div>
        {/if}

        <!-- History Section -->
        {#if challenges.length > 0}
            <div class="bg-white rounded-lg shadow-sm border border-gray-200">
                <div class="flex items-center justify-between p-6 border-b border-gray-200">
                    <div class="flex items-center gap-2">
                        <Clock class="w-5 h-5 text-gray-500"/>
                        <h2 class="text-lg font-semibold text-gray-900">History</h2>
                        <span class="bg-gray-100 text-gray-600 text-sm px-2 py-1 rounded-full">
                            {challenges.length}
                        </span>
                    </div>
                    <button
                        onclick={clearHistory}
                        class="text-gray-500 hover:text-red-500 text-sm font-medium transition-colors flex items-center gap-1"
                        aria-label="Clear History"
                    >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                        Clear
                    </button>
                </div>
                <div class="divide-y divide-gray-200">
                    {#each challenges.slice(1) as challenge (challenge.id)}
                        <ChallengeCard
                            {challenge}
                            onExpand={() => { expandedChallenge = challenge; showExpandedView = true; }}
                            onCopy={() => copyChallenge(challenge)}
                            onShare={() => shareChallenge(challenge)}
                            onDelete={() => deleteChallenge(challenge.id)}
                        />
                    {/each}
                </div>
            </div>
        {:else}
            <!-- Empty History State -->
            <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
                <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Clock class="w-8 h-8 text-gray-400"/>
                </div>
                <h3 class="text-lg font-medium text-gray-900 mb-2">You're one click away from your first challenge</h3>
                <p class="text-gray-500 mb-6">
                    Pick a combination above and generate your first software engineering prompt.
                </p>
                <div class="text-sm text-gray-400">
                    💡 Tip: Mixing different settings can surprise you with unique real-world cases!
                </div>
            </div>
        {/if}
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
                {#if browser}
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

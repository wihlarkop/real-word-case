<script>
    let {
        show = $bindable(false),
        type = 'copy',
        challengeTitle = '',
        onOpenNewTab = null
    } = $props();

    // Auto-dismiss after 4 seconds
    $effect(() => {
        if (show) {
            const timer = setTimeout(() => {
                show = false;
            }, 4000);

            return () => clearTimeout(timer);
        }
    });

    function handleClose() {
        show = false;
    }

    function handleOpenNewTab() {
        if (onOpenNewTab) {
            onOpenNewTab();
        }
        show = false;
    }
</script>

{#if show}
    <div class="fixed top-4 right-4 z-50 animate-slide-in">
        <div class="bg-white rounded-lg shadow-lg border border-gray-200 p-4 max-w-sm">
            <div class="flex items-start justify-between">
                <div class="flex-1">
                    <h3 class="font-medium text-gray-900 mb-1">
                        {type === 'copy' ? 'Challenge copied' : 'Challenge URL copied'}
                    </h3>
                    <p class="text-sm text-gray-600">
                        {#if type === 'copy'}
                            The "{challengeTitle}" challenge is in your clipboard now
                        {:else}
                            The challenge "{challengeTitle}" has its own page now
                        {/if}
                    </p>

                    {#if type === 'share'}
                        <button
                                onclick={handleOpenNewTab}
                                class="text-red-500 hover:text-red-600 text-sm font-medium mt-2 inline-block"
                        >
                            Open in a new tab
                        </button>
                    {/if}
                </div>

                <button
                        onclick={handleClose}
                        class="ml-4 text-gray-400 hover:text-gray-600 flex-shrink-0"
                        aria-label="Close"
                >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>
            </div>
        </div>
    </div>
{/if}

<style>
    @keyframes slide-in {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    .animate-slide-in {
        animation: slide-in 0.3s ease-out;
    }
</style>

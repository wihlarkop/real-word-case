<script>
  export let show = false;
  export let onClose = () => {};
</script>

{#if show}
  <div class="bg-orange-50 border-l-4 border-orange-400 p-4 mx-6 mt-4 rounded-r-lg">
    <div class="flex items-start justify-between">
      <div class="flex">
        <div class="ml-3">
          <h3 class="text-sm font-medium text-orange-800">
            Oops! There was a problem connecting to our server.
          </h3>
          <div class="mt-1 text-sm text-orange-700">
            <p>We couldn't generate a new challenge due to a temporary server issue. Please try again shortly.</p>
            <p>If this keeps happening, contact support or check your connection.</p>
          </div>
        </div>
      </div>
      <div class="flex-shrink-0 ml-4">
        <button
          on:click={onClose}
          class="text-orange-400 hover:text-orange-600"
          aria-label="Close"
        >
          <span class="sr-only">Close</span>
          <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clip-rule="evenodd"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
{/if}

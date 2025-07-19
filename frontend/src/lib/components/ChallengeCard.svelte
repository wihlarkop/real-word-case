<script lang="ts">
  import CustomMarkdown from './CustomMarkdown.svelte';
  import { Copy, Trash2, RotateCcw } from 'lucide-svelte';
  import type { Challenge } from '../types';
  export let challenge: Challenge;
  export let isLatest: boolean = false;
  export let onExpand: () => void = () => {};
  export let onCopy: () => void = () => {};
  export let onShare: (() => void) | null = null;
  export let onDelete: (() => void) | null = null;
  export let onRegenerate: (() => void) | null = null;
</script>

<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-8 mb-8">
  <CustomMarkdown content={challenge.text} variant={isLatest ? 'default' : 'default'} className="mb-6" />
  <div class="flex items-center justify-between mb-6">
    <div class="flex items-center gap-4 text-sm text-gray-500">
      <span>{challenge.industry}</span>
      <span>•</span>
      <span>{challenge.date}</span>
    </div>
    <div class="flex items-center gap-2">
      <button on:click={onExpand} class="p-2 text-gray-400 hover:text-gray-600 transition-colors" title="Expand" aria-label="Expand Challenge">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
        </svg>
      </button>
      <button on:click={onCopy} class="p-2 text-gray-400 hover:text-gray-600 transition-colors" title="Copy" aria-label="Copy Challenge">
        <Copy class="w-4 h-4" />
      </button>
      <button on:click={onShare} class="p-2 text-gray-400 hover:text-gray-600 transition-colors" title="Share" aria-label="Share Challenge">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
        </svg>
      </button>
      {#if isLatest && onRegenerate}
        <button on:click={onRegenerate} class="p-2 text-gray-400 hover:text-gray-600 transition-colors" title="Regenerate" aria-label="Regenerate Challenge">
          <RotateCcw class="w-4 h-4" />
        </button>
      {/if}
      {#if !isLatest}
        <button on:click={onDelete} class="p-2 text-gray-400 hover:text-red-500 transition-colors" title="Delete" aria-label="Delete Challenge">
          <Trash2 class="w-4 h-4" />
        </button>
      {/if}
    </div>
  </div>
</div>

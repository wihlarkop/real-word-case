<script lang="ts">
    export let options: { value: string; label: string }[] = [];
    export let value: string = '';
    export let icon: string = '';
    export let placeholder: string = 'Select an option';
    export let disabled: boolean = false;
    export let className: string = '';
</script>

<div class="relative w-full">
    {#if icon}
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <span class="text-gray-400">{@html icon}</span>
        </div>
    {/if}
    <select
            bind:value
            class={`w-full ${icon ? 'pl-10' : 'pl-4'} pr-10 py-3 border-2 border-gray-200 rounded-lg bg-white text-gray-800 font-medium focus:ring-2 focus:ring-red-400 focus:border-red-500 transition-all duration-150 appearance-none cursor-pointer ${disabled ? 'opacity-50 cursor-not-allowed' : ''} ${className}`}
            {disabled}
    >
        <option value="">{placeholder}</option>
        {#each options as option}
            <option value={option.value || option}>
                {option.label || option}
            </option>
        {/each}
    </select>
    <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-4">
        <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
        </svg>
    </div>
</div>

<style>
    select {
        -webkit-appearance: none;
        -moz-appearance: none;
        appearance: none;
        background: white;
    }

    select:focus {
        outline: none;
        border-color: #ef4444;
        box-shadow: 0 0 0 2px #fecaca;
    }
</style>

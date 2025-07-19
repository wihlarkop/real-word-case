<script>
  import EnhancedSelect from './EnhancedSelect.svelte';
  export let categories;
  export let selectedCategory;
</script>
<div class="flex flex-col sm:flex-row gap-4 mb-6">
  <EnhancedSelect
    bind:value={selectedCategory.industry}
    options={categories.industries}
    placeholder="Select Industry"
    icon={`<svg class=\"h-5 w-5\" fill=\"none\" viewBox=\"0 0 24 24\" stroke=\"currentColor\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4\" /></svg>`}
    className="flex-1"
  />
  <EnhancedSelect
    bind:value={selectedCategory.role}
    options={categories.roles}
    placeholder="Select Role"
    icon={`<svg class=\"h-5 w-5\" fill=\"none\" viewBox=\"0 0 24 24\" stroke=\"currentColor\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z\" /></svg>`}
    className="flex-1"
  />
  <EnhancedSelect
    bind:value={selectedCategory.difficulty}
    options={categories.difficulties}
    placeholder="Select Difficulty"
    icon={`<svg class=\"h-5 w-5\" fill=\"none\" viewBox=\"0 0 24 24\" stroke=\"currentColor\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z\" /></svg>`}
    className="flex-1"
  />
</div>

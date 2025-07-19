<script lang="ts">
    import Markdown from 'svelte-exmarkdown';
    import { gfmPlugin } from 'svelte-exmarkdown/gfm';
    
    export let content: string = '';
    export let variant: 'default' | 'expanded' | 'compact' = 'default'; 
    export let className: string = '';
    
    const plugins = [gfmPlugin()];
    
    // Preprocessing untuk konten yang lebih baik
    function preprocessContent(text: string): string {
        // Tambahkan emoji untuk section headers tertentu
        text = text.replace(/^## (Requirements?|Requirement)/gmi, '## 📋 $1');
        text = text.replace(/^## (Technical|Tech)/gmi, '## ⚙️ $1');
        text = text.replace(/^## (Business|Goal)/gmi, '## 🎯 $1');
        text = text.replace(/^## (Challenge|Problem)/gmi, '## 🚀 $1');
        text = text.replace(/^## (Solution|Approach)/gmi, '## 💡 $1');
        text = text.replace(/^## (Timeline|Schedule)/gmi, '## ⏰ $1');
        text = text.replace(/^## (Team|Resources)/gmi, '## 👥 $1');
        text = text.replace(/^## (Deliverable)/gmi, '## 📦 $1');
        
        // Highlight important phrases
        text = text.replace(/\*\*(IMPORTANT|CRITICAL|URGENT)\*\*/gi, '**🔥 $1**');
        text = text.replace(/\*\*(NOTE|TIP|HINT)\*\*/gi, '**💡 $1**');
        
        return text;
    }
    
    $: processedContent = preprocessContent(content);
    $: variantClass = {
        'default': 'markdown-default',
        'expanded': 'markdown-expanded', 
        'compact': 'markdown-compact'
    }[variant];
</script>

<div class="custom-markdown {variantClass} {className}">
    <Markdown md={processedContent} {plugins} />
</div>

<style>
    :global(.custom-markdown) {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        line-height: 1.7;
        color: #374151;
    }
    
    /* Default variant */
    :global(.markdown-default) {
        font-size: 1rem;
    }
    
    :global(.markdown-default h1) {
        font-size: 1.875rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 1.5rem;
        margin-top: 2rem;
        border-bottom: 3px solid #ef4444;
        padding-bottom: 0.5rem;
    }
    
    :global(.markdown-default h2) {
        font-size: 1.5rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 1rem;
        margin-top: 1.5rem;
        border-bottom: 1px solid #e5e7eb;
        padding-bottom: 0.25rem;
    }
    
    :global(.markdown-default h3) {
        font-size: 1.25rem;
        font-weight: 600;
        color: #ef4444;
        margin-bottom: 0.75rem;
        margin-top: 1.25rem;
    }
    
    :global(.markdown-default p) {
        margin-bottom: 1rem;
        text-align: justify;
    }
    
    :global(.markdown-default ul, .markdown-default ol) {
        margin-bottom: 1rem;
        padding-left: 1.5rem;
    }
    
    :global(.markdown-default li) {
        margin-bottom: 0.5rem;
        line-height: 1.6;
    }
    
    :global(.markdown-default ul li::marker) {
        content: "▸ ";
        color: #ef4444;
    }
    
    :global(.markdown-default strong) {
        font-weight: 600;
        color: #111827;
        background-color: #fef3c7;
        padding: 0.125rem 0.25rem;
        border-radius: 0.25rem;
    }
    
    :global(.markdown-default em) {
        font-style: italic;
        color: #6b7280;
    }
    
    :global(.markdown-default code) {
        background-color: #f3f4f6;
        color: #ef4444;
        padding: 0.125rem 0.375rem;
        border-radius: 0.25rem;
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: 0.875rem;
    }
    
    :global(.markdown-default pre) {
        background-color: #1f2937;
        color: #f9fafb;
        padding: 1rem;
        border-radius: 0.5rem;
        overflow-x: auto;
        margin: 1rem 0;
        border-left: 4px solid #ef4444;
    }
    
    :global(.markdown-default pre code) {
        background-color: transparent;
        color: #10b981;
        padding: 0;
    }
    
    :global(.markdown-default blockquote) {
        border-left: 4px solid #ef4444;
        padding-left: 1rem;
        margin: 1rem 0;
        font-style: italic;
        color: #6b7280;
        background-color: #fef2f2;
        padding: 1rem;
        border-radius: 0 0.5rem 0.5rem 0;
    }
    
    /* Expanded variant */
    :global(.markdown-expanded) {
        text-align: center;
    }
    
    :global(.markdown-expanded h1) {
        font-size: 3rem;
        font-weight: 300;
        line-height: 1.2;
        margin-bottom: 2rem;
    }
    
    :global(.markdown-expanded p) {
        font-size: 1.25rem;
        line-height: 1.8;
        margin-bottom: 1.5rem;
        max-width: 60ch;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Compact variant */
    :global(.markdown-compact) {
        font-size: 0.875rem;
        line-height: 1.5;
    }
    
    :global(.markdown-compact h1) {
        font-size: 1.25rem;
        margin-bottom: 0.75rem;
    }
    
    :global(.markdown-compact h2) {
        font-size: 1.125rem;
        margin-bottom: 0.5rem;
    }
    
    :global(.markdown-compact p) {
        margin-bottom: 0.75rem;
    }
    
    /* Animation */
    :global(.custom-markdown) {
        animation: slideInUp 0.4s ease-out;
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Responsive */
    @media (max-width: 640px) {
        :global(.markdown-default h1) {
            font-size: 1.5rem;
        }
        
        :global(.markdown-default h2) {
            font-size: 1.25rem;
        }
        
        :global(.markdown-expanded h1) {
            font-size: 2rem;
        }
        
        :global(.markdown-expanded p) {
            font-size: 1.125rem;
        }
    }
</style>

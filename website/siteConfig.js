const siteConfig = {
    title: 'Codewatch',
    tagline: 'Monitor and manage deeply customizable metrics about your python code using ASTs',
    // For deploy
    cname: 'codewatch.io',
    url: 'https://codewatch.io',
    baseUrl: '/',
    projectName: 'codewatch',
    organizationName: 'tophat',
    // End deploy options
    headerLinks: [
        { doc: 'overview', label: 'Docs' },
        { href: "https://github.com/tophat/codewatch", label: "GitHub" },
    ],
    headerIcon: 'img/codewatch.png',
    footerIcon: 'img/codewatch.png',
    favicon: 'img/codewatch.png',
    colors: {
        primaryColor: '#58b4c5',
        secondaryColor: '#272822',
    },
    customDocsPath: 'docs',
    gaTrackingId: '',

    copyright: 'Top Hat Open Source',

    highlight: {
        // Highlight.js theme to use for syntax highlighting in code blocks.
        theme: 'default',
    },

    // Add custom scripts here that would be placed in <script> tags.
    scripts: ['https://buttons.github.io/buttons.js'],
    onPageNav: 'separate', // On page navigation for the current documentation page.
    cleanUrl: true, // No .html extensions for paths.

    // Open Graph and Twitter card images.
    ogImage: 'img/codewatch.png',
    twitterImage: 'img/codewatch.png',

    // Show documentation's last contributor's name.
    enableUpdateBy: true,
}

module.exports = siteConfig

const root = document.documentElement;
function indexReactive(){
    return{    
        currentThemeIndex:0,
        themes:['Dark','Light','Snow'],

        init() {
            this.currentThemeIndex = parseInt(localStorage.getItem('libroTheme') || 0) ;
            root.setAttribute('data-theme', this.themes[this.currentThemeIndex]);
        },

        toggleThemes(){
            this.currentThemeIndex = (this.currentThemeIndex+1)%3;
            root.setAttribute('data-theme', this.themes[this.currentThemeIndex]);
            localStorage.setItem('libroTheme', this.currentThemeIndex);
        },
    }
}

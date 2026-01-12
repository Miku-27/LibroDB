function loginHandler() {
    return {
        formData: {
            usermail: '',
            password: ''
        },
        loading: false,
        async submitLogin() {
            this.loading = true;
            const [status,data] = await requestBackend('/api/auth/token','POST',this.formData)
            if (status){
                window.location.href = '/library';
            }
            this.loading = false;
        },

        currentThemeIndex:0,
        themes:['Dark','Light','Snow'],

        init() {
            this.currentThemeIndex = parseInt(localStorage.getItem('libroTheme') || 0) ;
            root.setAttribute('data-theme', this.themes[this.currentThemeIndex]);
        },
    }
}


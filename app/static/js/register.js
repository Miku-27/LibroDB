function registerHandler() {
    return {
        formData: {
            username:'',
            usermail: '',
            password: ''
        },
        loading: false,
        async submitRegister() {
            this.loading = true;
            const backendResponse = await requestBackend('/api/auth/user','POST',this.formData)
            if (backendResponse != null){
                window.location.href = '/login';
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


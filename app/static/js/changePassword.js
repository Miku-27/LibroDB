const urlParams = new URLSearchParams(window.location.search);
const token = urlParams.get('token');

function changePasswordReactive() {
    return {
        show: false,
        formData: {
            resetToken: token,
            newPassword: ''
        },
        loading: false,
        showErrorMsg:false,
        confirmPassword:null,

        passwordsMatch() {
            if (this.formData.newPassword == this.confirmPassword){
                this.showErrorMsg=false;
                return true;   
            }
            this.showErrorMsg=true;
            return false;
        },

        async submitPassword() {
            this.loading = true;
            if (!this.passwordsMatch()){
                this.loading=false;
                return;
            }
            const backendResponse = await requestBackend('/api/auth/password-reset','PATCH',this.formData)
            if (backendResponse != null){
                window.location.href = '/login';
            }
        },

        currentThemeIndex:0,
        themes:['Dark','Light','Snow'],

        init() {
            this.currentThemeIndex = parseInt(localStorage.getItem('libroTheme') || 0) ;
            root.setAttribute('data-theme', this.themes[this.currentThemeIndex]);
        },
    }
}

function forgetPasswordReactive() {
    return {
        formData: {
            usermail: ''
        },
        loading: false,

        async submitData() {
            this.loading = true;
            await requestBackend('/api/auth/password-reset',"POST",this.formData);
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
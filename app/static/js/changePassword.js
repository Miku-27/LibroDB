const urlParams = new URLSearchParams(window.location.search);
const token = urlParams.get('token');

document.addEventListener('alpine:init', () => {
    Alpine.data('passwordResetReactive', () => ({
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
            const backendResponse = await requestBackend('/api/auth/password-reset','POST',this.formData)
            if (backendResponse != null){
                window.location.href = '/login';
            }
        }
    }))
})

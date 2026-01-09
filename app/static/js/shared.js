async function requestBackend(url,method,dataToSend=null,contentType='application/json'){ 
    const csrfToken = getCookie('csrf_access_token');

    const options = {
        method: method,
        headers: {
            'Content-Type': contentType,
            'X-CSRF-TOKEN': csrfToken
        }
    };
    
    if (dataToSend) {
        options.body = JSON.stringify(dataToSend);
    }
    
    try {
        const httpResponse = await fetch(url, options);
        response = await httpResponse.json()
        
        if (response.status === 401) {
            window.dispatchEvent(new CustomEvent('show-toast', { 
                detail: {
                    message: response.msg,
                    type: response.success
                }     
            }));
            setTimeout(() => {
                window.location.href = "/login";
            }, 2000);
        }
        
        if (httpResponse.ok && response.success === true && response.data != null){
            return [true,response.data];
        }
        else if(response.success === true && response.data == null){
            window.dispatchEvent(new CustomEvent('show-toast', { 
                detail: {
                    message: response.msg,
                    type: response.success
                }     
            }));
            return [true,null];
        }
        else{
            window.dispatchEvent(new CustomEvent('show-toast', { 
                detail: {
                    message: response.msg,
                    type: response.success
                }  
            }));
            return [false,null];
        }
        
    } catch (error) {
        console.error("Network or Setup Error:", error);
        window.dispatchEvent(new CustomEvent('show-toast', { 
            detail: {
                message: response.msg,
                type: response.success
            }  
        }));
        return [false,null];
    }
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}


function customToastMessage(message,success){
    window.dispatchEvent(new CustomEvent('show-toast', { 
        detail: {
            message: message,
            type: success
        }     
    }));
}


// NAVBAR RELATED JS CODE:
const root = document.documentElement;
function navbarReactive(){
    return{
        navbarOpen: false,
        
        currentThemeIndex:0,
        themes:['Dark','Light','Forest'],

        init() {
            this.currentThemeIndex = parseInt(localStorage.getItem('libroTheme') || 0) ;
            root.setAttribute('data-theme', this.themes[this.currentThemeIndex]);
        },

        toggleThemes(){
            this.currentThemeIndex = (this.currentThemeIndex+1)%3;
            root.setAttribute('data-theme', this.themes[this.currentThemeIndex]);
            localStorage.setItem('libroTheme', this.currentThemeIndex);
        },

        async logoutUser(){
            const backendResponse = await requestBackend('/api/auth/logout','POST')
            if (backendResponse != null){
                window.location.href = '/login';
            }
        }
    }
}

export const isLoggedIn = () => {
    const token = localStorage.getItem('accessToken')
    return token !== undefined && token !== ''
}

export const loggout = () => {
    localStorage.removeItem('accessToken')
}

export const localStorageToJson = () => {
    let storageObject = {};

    // Iterar sobre todas as chaves do localStorage
    for (let i = 0; i < localStorage.length; i++) {
        // Obter a chave pela posição
        let key = localStorage.key(i);
        
        // Obter o valor associado à chave
        let value = localStorage.getItem(key);
        
        // Tentar converter o valor para JSON, se for uma string JSON
        try {
            value = JSON.parse(value);
        } catch (e) {
        // Se não for JSON, manter o valor como string
        }
        
        // Adicionar ao objeto
        storageObject[key] = value;
    }

    // Exibir o objeto montado como JSON
    return storageObject
}
export const can = (action) => {
    if (!action) return true
    let _actions = localStorage.getItem('permissions')
    if (!_actions) return false
    const actions = JSON.parse(_actions)
    const actions_list = actions.map(obj => `${obj.action}-${obj.subject}`)
    return actions_list.includes(action)
}
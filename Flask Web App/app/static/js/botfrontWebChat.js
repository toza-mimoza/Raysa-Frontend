//window.onload = WebChat.open; 
profileAvatarUrl = ""

function setProfileAvatarUrl(url) {
    profileAvatarUrl=url;   // The function returns the product of p1 and p2
}
WebChat.default.init({
    selector: "#webchat",
    initPayload: "main menu",
    interval: 1000,
    customData: {"language": "en"}, // arbitrary custom data. Stay minimal as this will be added to the socket
    socketUrl: "http://localhost:5005/",// "http://localhost:5005/",
    socketPath: "/socket.io/",
    title: "Raysa Cluster",
    subtitle: "",
    inputTextFieldHint: "Type a message",
    embedded: false,
    showFullScreenButton: true,
    showMessageDate: false,
    hideWhenNotConnected: false,
    displayUnreadCount: true,
    profileAvatar: profileAvatarUrl,

    params: {"storage": "session"} // can be set to "local"  or "session". details in storage section.
})

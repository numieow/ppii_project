class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.messages = [{ name: "SALAD", message: "Bonjour je suis Salad" }];  // la liste des message est initialisée avec un message du bot ( ?proposant différentes questions standards ?) 
    }

    display() {
        const {openButton, chatBox, sendButton} = this.args;            //créé un objet chatbox

        openButton.addEventListener('click', () => this.toggleState(chatBox))   // Si on click sur le bouton de discussion on lance la methode de changement d'état (actif -inactif)

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))  // Si on click sur le bouton d'envoi on lance la methode d'envoi : onSendButtone

        const recu = chatBox.querySelector('input');        //recu est l'input user dans la zone txt
        recu.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {                  //Si on appuie sur Entré on lance la methode d'envoi 
                this.onSendButton(chatBox)
            }
        })
    }

    toggleState(chatbox) {
        this.state = !this.state;               // change l'état (ouvert/fermé)

        // show or hides the box
        if(this.state) { 
            chatbox.classList.add('chatbox--active')    //Si l'etat est actif on l'ajoute a la liste des class
        } else {
            chatbox.classList.remove('chatbox--active') // Sinon on l'enlève de la liste des classes
        }
        this.updateChatText(chatbox)
    }
    onSendButton(chatbox) { //Quand un message est envoyé (appui sur le bouton d'envoi)
        var textField = chatbox.querySelector('input');     // On récupère le message qui vient d'être envoyé
        let text1 = textField.value
        if (text1 === "") {
            return;                                         //Si on a appuyé sans envoyer de message, il ne se passe rien
        }

        let msg1 = { name: "User", message: text1 }         // créé a partir de l'input user le message à afficher dans la fenêtre
        this.messages.push(msg1);                           // Affiche ce message
        //$SCRIPT_ROOT + '/predict'//
        //'http://127.0.0.1:5000/predict'//
        fetch('http://127.0.0.1:5000/predict', {  //On envoie un post a la route /predict
            method: 'POST',
            body: JSON.stringify({ message: text1 }), //le contenu est le message créé au dessus dont la clé est 'message'
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json'
            },
          })
          .then(r => r.json())
          .then(r => {
            let msg2 = { name: "SALAD", message: r.answer };
            this.messages.push(msg2);
            this.updateChatText(chatbox)
            textField.value = ''

        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox)
            textField.value = ''
          });
    }
    updateChatText(chatbox) {       //On va mettre a jour la conversation affichée en ajoutant le nouveau message
        console.log(this.messages)
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {         //Pour les messages de la conversation
            if (item.name === "SALAD")                                          // si le message vient de SALAD 
            {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>' //on ajoute le message dans le html en donnant la class visitor pour avoir la bonne couleur après css
            }
            else
            {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>' //Sinon on le met avec la classe operator pour avoir la bonne couleur après css
            }
          });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }

}
console.log("printttttttt")
const chatbox = new Chatbox();
chatbox.display();


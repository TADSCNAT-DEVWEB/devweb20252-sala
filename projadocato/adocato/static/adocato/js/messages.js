  // Função para fechar notificação individual
        function closeNotification(deleteButton) {
            const notification = deleteButton.parentNode;
            notification.style.display = 'none';
            notification.remove();
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            // Fecha depois de 5 segundos
            setTimeout(() => {
                const messagesContainer = document.getElementById('messages-container');
                if (messagesContainer) {
                    messagesContainer.style.display = 'none';
                    messagesContainer.remove();
                }
            }, 5000);
        });
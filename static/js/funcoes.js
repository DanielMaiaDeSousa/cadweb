// Função para carregar a imagem no canvas
function loadImage(base64Image,target_canvas) {

            var img = new Image();
            img.src = base64Image;
           

            img.onload = function() {
                const canvas = document.getElementById(target_canvas);
                const ctx = canvas.getContext('2d');
                var canvasWidth = canvas.width;
                var canvasHeight = canvas.height;
    
                // Dimensões da imagem original
                var imgWidth = img.width;
                var imgHeight = img.height;

                // Calcula a proporção para redimensionamento
                var scaleWidth = canvasWidth / imgWidth;
                var scaleHeight = canvasHeight / imgHeight;
                var scale = Math.min(scaleWidth, scaleHeight); // Mantém a proporção

                // Novas dimensões da imagem
                var newWidth = imgWidth * scale;
                var newHeight = imgHeight * scale;

                // Calcula a posição para centralizar a imagem no canvas
                var offsetX = (canvasWidth - newWidth) / 2;
                var offsetY = (canvasHeight - newHeight) / 2; 

                // Limpa o canvas e desenha a imagem redimensionada
                ctx.clearRect(0, 0, canvasWidth, canvasHeight);
                ctx.drawImage(img, offsetX, offsetY, newWidth, newHeight);
            };

        }

// static/js/funcoes.js

// Placeholder SVG (sem imagem)
var PRODUCT_PLACEHOLDER = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="56" height="56"><rect width="100%" height="100%" fill="%23f8f9fa"/><text x="50%" y="50%" font-size="10" text-anchor="middle" dominant-baseline="central" fill="%23888">sem imagem</text></svg>';

function autoComplete(inputSelector) {
    var inputElement = $(inputSelector);
    var buscaUrl = inputElement.data('url');
    var hiddenSelector = inputElement.data('hidden');

    $(inputSelector).autocomplete({
        source: function(request, response) {
            $.ajax({
                url: buscaUrl,
                dataType: "json",
                data: { q: request.term },
                success: function(data) {
                    response($.map(data, function(item) {
                        return {
                            label: item.nome,
                            value: item.nome,
                            id: item.id,
                            preco: item.preco, // Capturamos o preço do JSON
                            img_base64: item.img_base64 // Capturamos a imagem, quando houver
                        };
                    }));
                }
            });
        },
        select: function(event, ui) {
            $(hiddenSelector).val(ui.item.id);

            // Atualiza texto acessível do preview
            $('#produto_preview').text(ui.item.nome || '');

            // Preenche preço, se houver
            if (ui.item.preco) {
                $('#id_preco').val(ui.item.preco.replace('.', ','));
                $('#id_preco').trigger('input');
            }

            // Mostra preview da imagem do produto, se disponível (ou placeholder)
            if (ui.item.img_base64) {
                $('#img_preview_pedido').removeClass('placeholder').attr('src', ui.item.img_base64).attr('alt', ui.item.label || 'Pré-visualização');
            } else {
                $('#img_preview_pedido').addClass('placeholder').attr('src', PRODUCT_PLACEHOLDER).attr('alt', 'Sem imagem');
            }
            $('#preview_container').show().attr('aria-hidden', 'false');
        }
    });

    // Esconde preview se o campo for limpo manualmente
    inputElement.on('input', function() {
        if (!$(this).val()) {
            $('#preview_container').hide().attr('aria-hidden', 'true');
            $('#img_preview_pedido').attr('src', '').attr('alt', '').removeClass('placeholder');
            $(hiddenSelector).val('');
            $('#produto_preview').text('');
        }
    });
}        
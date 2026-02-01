// static/js/funcoes.js

/**
 * Função para carregar e redimensionar a imagem no canvas
 */
function loadImage(base64Image, target_canvas) {
    var img = new Image();
    img.src = base64Image;

    img.onload = function() {
        const canvas = document.getElementById(target_canvas);
        const ctx = canvas.getContext('2d');
        var canvasWidth = canvas.width;
        var canvasHeight = canvas.height;

        var imgWidth = img.width;
        var imgHeight = img.height;

        var scaleWidth = canvasWidth / imgWidth;
        var scaleHeight = canvasHeight / imgHeight;
        var scale = Math.min(scaleWidth, scaleHeight);

        var newWidth = imgWidth * scale;
        var newHeight = imgHeight * scale;

        var offsetX = (canvasWidth - newWidth) / 2;
        var offsetY = (canvasHeight - newHeight) / 2;

        ctx.clearRect(0, 0, canvasWidth, canvasHeight);
        ctx.drawImage(img, offsetX, offsetY, newWidth, newHeight);
    };
}

// Placeholder SVG para produtos sem imagem
var PRODUCT_PLACEHOLDER = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="56" height="56"><rect width="100%" height="100%" fill="%23f8f9fa"/><text x="50%" y="50%" font-size="10" text-anchor="middle" dominant-baseline="central" fill="%23888">sem imagem</text></svg>';

/**
 * Configuração do Autocomplete para produtos com preview de imagem e preço
 */
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
                            preco: item.preco,
                            img_base64: item.img_base64
                        };
                    }));
                }
            });
        },
        select: function(event, ui) {
            $(hiddenSelector).val(ui.item.id);
            $('#produto_preview').text(ui.item.nome || '');

            if (ui.item.preco) {
                $('#id_preco').val(ui.item.preco.replace('.', ','));
                $('#id_preco').trigger('input');
            }

            if (ui.item.img_base64) {
                $('#img_preview_pedido').removeClass('placeholder').attr('src', ui.item.img_base64).attr('alt', ui.item.label || 'Pré-visualização');
            } else {
                $('#img_preview_pedido').addClass('placeholder').attr('src', PRODUCT_PLACEHOLDER).attr('alt', 'Sem imagem');
            }
            $('#preview_container').show().attr('aria-hidden', 'false');
        }
    });

    inputElement.on('input', function() {
        if (!$(this).val()) {
            $('#preview_container').hide().attr('aria-hidden', 'true');
            $('#img_preview_pedido').attr('src', '').attr('alt', '').removeClass('placeholder');
            $(hiddenSelector).val('');
            $('#produto_preview').text('');
        }
    });
}

/**
 * NOVO: Lógica para cálculo de parcelas em tempo real
 * Esta função deve ser chamada no $(document).ready() da página de pagamentos
 */
function configurarCalculoParcelas() {
    const selectTipo = document.getElementById('id_tipo_pagamento');
    const divParcelas = document.getElementById('div_parcelas');
    const divValorParcela = document.getElementById('div_valor_parcela');
    const campoParcelas = document.getElementById('id_parcelas');
    const campoValorTotal = document.getElementById('id_valor_pagamento');
    const campoValorParcelaView = document.getElementById('id_valor_parcela_view');

    // Verifica se os elementos existem na página atual para evitar erros
    if (!selectTipo || !campoValorTotal) return;

    function atualizarCalculo() {
        const isParcelado = selectTipo.value === 'parcelado';
        
        // Controla a visibilidade dos blocos de parcelamento
        if (divParcelas) divParcelas.style.display = isParcelado ? 'block' : 'none';
        if (divValorParcela) divValorParcela.style.display = isParcelado ? 'block' : 'none';

        const valorTotal = parseFloat(campoValorTotal.value) || 0;
        const numParcelas = parseInt(campoParcelas.value) || 1;

        if (isParcelado && valorTotal > 0 && numParcelas > 0) {
            const valorParcela = valorTotal / numParcelas;
            // Formata o valor calculado para moeda brasileira
            campoValorParcelaView.value = valorParcela.toLocaleString('pt-BR', {
                style: 'currency',
                currency: 'BRL'
            });
        } else if (campoValorParcelaView) {
            campoValorParcelaView.value = "";
        }
    }

    // Registra os ouvintes de evento para atualização instantânea
    selectTipo.addEventListener('change', atualizarCalculo);
    campoParcelas.addEventListener('input', atualizarCalculo);
    campoValorTotal.addEventListener('input', atualizarCalculo);
    
    // Executa uma vez no carregamento para ajustar o estado inicial
    atualizarCalculo();
}
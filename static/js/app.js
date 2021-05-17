// Rentabilidade
function get_profitability(price, product_price) {
	const minimum_price = product_price - (product_price * 0.1);

	if (price > product_price)
		return 1;
	else if (price <= product_price && price >= minimum_price)
		return 0;
	else if (price < minimum_price)
		return -1;
}

function get_profitability_text(price, product_price) {
	const profitability = get_profitability(price, product_price);

	if (profitability > 0)
		return 'Ótima <span class="fa fa-angle-double-up text-success"></span>'
	else if (profitability == 0)
		return 'Boa <span class="fa fa-angle-up text-warning"></span>'

	return 'Ruim <span class="fa fa-angle-down text-danger"></span>'
}

function set_profitability_text(price, product_price) {
	var text = '<span class="text-muted">(Selecione o produto e o preço para exibir)</span>';
	
	if (price && product_price)
		text = get_profitability_text(price, product_price);

	$('.profitability').html(text);
}

$(function() {
	// mask money
    const input = SimpleMaskMoney.setMask('.money');

	// rentabilidade
	$('#id_product_id').on('change', function() {
		const price = input.formatToNumber();
		const product_price = parseFloat($(this).children('option:selected').data('price'));
		$('#product-price').text(SimpleMaskMoney.formatToCurrency(product_price));
		set_profitability_text(price, product_price);
	});

	$('#id_price').on('input', function() {
		const price = input.formatToNumber();
		const product_price = parseFloat($('#id_product_id option:selected').data('price'));
		set_profitability_text(price, product_price)
	});

	const price = input.formatToNumber();
	const product_price = parseFloat($('#id_product_id option:selected').data('price'));
	$('#product-price').text(SimpleMaskMoney.formatToCurrency(product_price));
	set_profitability_text(price, product_price);
});

const DEFAULT_NUMBER = '5511999999999';

function sanitizePhone(value: string): string {
  const onlyDigits = value.replace(/\D/g, '');
  return onlyDigits || DEFAULT_NUMBER;
}

function getWhatsAppNumber(): string {
  const value = (import.meta.env.PUBLIC_WHATSAPP_NUMBER || DEFAULT_NUMBER) as string;
  return sanitizePhone(value);
}

export function buildWhatsAppUrl(productName?: string): string {
  const number = getWhatsAppNumber();
  const message = productName
    ? `Olá! Tenho interesse no produto \"${productName}\" para revenda. Pode me passar mais detalhes?`
    : 'Olá! Vim pelo catálogo e quero mais informações sobre as molduras para revenda.';

  return `https://wa.me/${number}?text=${encodeURIComponent(message)}`;
}

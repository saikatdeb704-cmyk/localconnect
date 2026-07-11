// Email validation
export const validateEmail = (email: string): boolean => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
};

// Phone validation (Indian format)
export const validatePhone = (phone: string): boolean => {
  const re = /^[6-9]\d{9}$/;
  return re.test(phone.replace(/\D/g, ''));
};

// Pincode validation (Indian)
export const validatePincode = (pincode: string): boolean => {
  const re = /^[0-9]{6}$/;
  return re.test(pincode);
};

// Password validation
export const validatePassword = (password: string): boolean => {
  return password.length >= 8;
};

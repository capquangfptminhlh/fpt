(() => {
  const form = document.querySelector('[data-lead-form]');
  if (!form) return;

  const statusBox = document.querySelector('[data-lead-status]');
  const submitButton = form.querySelector('button[type="submit"]');
  const endpoint = document.querySelector('meta[name="lead-endpoint"]')?.content?.trim() || '';
  const needLabels = {
    family: 'Gia đình',
    multi: 'Nhà nhiều tầng',
    game: 'Game / streaming',
    office: 'Làm việc / kinh doanh',
    camera: 'Camera / smart home',
    other: 'Khác'
  };

  const params = new URLSearchParams(location.search);
  const addressInput = form.elements.address;
  const needInput = form.elements.need;
  if (addressInput && params.get('address')) addressInput.value = params.get('address');
  if (needInput && params.get('need')) needInput.value = params.get('need');

  const normalizePhone = (value) => value.replace(/[\s.()-]/g, '');
  const isPhoneValid = (value) => /^(?:\+84|0)\d{9,10}$/.test(normalizePhone(value));

  const setError = (field, message = '') => {
    if (!field) return;
    field.setAttribute('aria-invalid', message ? 'true' : 'false');
    const error = form.querySelector(`[data-error-for="${field.name}"]`);
    if (error) error.textContent = message;
  };

  const validate = () => {
    let ok = true;
    const name = form.elements.name;
    const phone = form.elements.phone;
    const address = form.elements.address;
    const consent = form.elements.consent;

    if (!name.value.trim() || name.value.trim().length < 2) {
      setError(name, 'Vui lòng nhập họ tên.');
      ok = false;
    } else setError(name);

    if (!isPhoneValid(phone.value)) {
      setError(phone, 'Số điện thoại chưa đúng định dạng.');
      ok = false;
    } else setError(phone);

    if (!address.value.trim() || address.value.trim().length < 4) {
      setError(address, 'Vui lòng nhập khu vực hoặc địa chỉ lắp đặt.');
      ok = false;
    } else setError(address);

    if (!consent.checked) {
      setError(consent, 'Bạn cần đồng ý để tiếp tục.');
      ok = false;
    } else setError(consent);

    return ok;
  };

  const payloadFromForm = () => ({
    name: form.elements.name.value.trim(),
    phone: normalizePhone(form.elements.phone.value),
    address: form.elements.address.value.trim(),
    need: needLabels[form.elements.need.value] || form.elements.need.value,
    note: form.elements.note.value.trim(),
    _honey: form.elements._honey?.value || '',
    _subject: 'Lead mới từ website tư vấn Internet FPT',
    _template: 'table',
    _url: location.href,
    page: location.href,
    created_at: new Date().toISOString()
  });

  const formatLead = (payload) => [
    `Họ tên: ${payload.name}`,
    `Điện thoại: ${payload.phone}`,
    `Địa chỉ: ${payload.address}`,
    `Nhu cầu: ${payload.need || 'Chưa chọn'}`,
    payload.note ? `Ghi chú: ${payload.note}` : null
  ].filter(Boolean).join('\n');

  const renderFallback = (payload) => {
    sessionStorage.setItem('fptLeadDraft', JSON.stringify(payload));
    if (!statusBox) return;
    statusBox.className = 'lead-status is-visible is-error';
    statusBox.innerHTML = `
      <strong>Chưa gửi được yêu cầu.</strong><br>
      Bạn có thể gọi CSKH hoặc sao chép thông tin vừa nhập để không phải nhập lại.
      <div class="lead-actions">
        <a class="call" href="tel:19006600">☎ Gọi 1900 6600</a>
        <button class="copy" type="button" data-copy-lead>Sao chép thông tin</button>
      </div>
    `;
    statusBox.querySelector('[data-copy-lead]')?.addEventListener('click', async (event) => {
      const text = formatLead(payload);
      try {
        await navigator.clipboard.writeText(text);
        event.currentTarget.textContent = 'Đã sao chép';
      } catch {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        textarea.remove();
        event.currentTarget.textContent = 'Đã sao chép';
      }
    });
    statusBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  };

  const renderSuccess = () => {
    if (!statusBox) return;
    statusBox.className = 'lead-status is-visible';
    statusBox.innerHTML = '<strong>Đã gửi yêu cầu.</strong><br>Thông tin của bạn đã được chuyển tới hộp thư nhận lead. Hãy giữ điện thoại để tiện liên hệ lại.';
    statusBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  };

  form.addEventListener('input', (event) => {
    const field = event.target;
    if (field?.name) setError(field);
  });

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!validate()) return;

    const payload = payloadFromForm();

    if (!endpoint) {
      renderFallback(payload);
      return;
    }

    submitButton.disabled = true;
    submitButton.textContent = 'Đang gửi…';
    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(payload)
      });
      const data = await response.json().catch(() => null);
      if (!response.ok || (data && data.success === false)) {
        throw new Error(data?.message || `HTTP ${response.status}`);
      }
      sessionStorage.removeItem('fptLeadDraft');
      renderSuccess();
      form.reset();
    } catch (error) {
      console.error('Lead submit failed', error);
      renderFallback(payload);
    } finally {
      submitButton.disabled = false;
      submitButton.textContent = 'Gửi yêu cầu tư vấn';
    }
  });
})();

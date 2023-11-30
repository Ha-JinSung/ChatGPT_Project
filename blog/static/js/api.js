async function getNewToken(refreshToken) {
  const response = await fetch('http://localhost:8000/accounts/api-auth/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          'refresh': refreshToken
      }),
  });

  const data = await response.json();
  return data.access;
}

async function fetchWithAutoRefresh(url, options) {
  const response = await fetch(url, options);

  if (!response.ok && response.status === 401) { // 토큰이 만료되었을 때의 상태 코드
      const refreshToken = localStorage.getItem('refreshToken'); // 로컬 스토리지에서 리프레시 토큰을 가져옵니다.
      const newToken = await getNewToken(refreshToken); // 새 토큰을 요청합니다.

      localStorage.setItem('accessToken', newToken); // 새 토큰을 로컬 스토리지에 저장합니다.

      options.headers['Authorization'] = `Bearer ${newToken}`; // 요청 헤더에 새 토큰을 설정합니다.
      return fetch(url, options); // 요청을 다시 보냅니다.
  }

  return response;
}

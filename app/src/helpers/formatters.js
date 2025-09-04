export const formatDateBrl = (date) => {
    const dataObj = new Date(date);
    dataObj.setHours(dataObj.getHours() - 3);
    const dataBr = dataObj.toLocaleString("pt-BR", {
        timeZone: "America/Sao_Paulo",
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
    });
    return dataBr;
}


export function toUTC(date) {
    return new Date(Date.UTC(
      date.getFullYear(),
      date.getMonth(),
      date.getDate(),
      date.getHours(),
      date.getMinutes(),
      date.getSeconds()
    ));
  }

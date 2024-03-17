const sendFile = async (item, ctx) => {
  if (item) {
    try {
      await ctx.replyWithDocument(item);
    } catch (e) {
      ctx.replyWithMarkdown(
        `error ${e.message}\n\n Try to download from [here](${item})\n\nThe file maybe Large*`,
      );
    }
  }
};

module.exports = {
  sendFile,
};

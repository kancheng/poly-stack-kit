-- Demo seed (optional) — run after schema.sql
-- Demo login: email demo@polystack.local / password: password
-- Hash below is bcrypt ($2y$) compatible with Laravel default; Django/Flask apps may need their own user or re-register.

SET NAMES utf8mb4;
USE `polystack`;

INSERT INTO `users` (`id`, `email`, `password_hash`, `name`) VALUES
  (1, 'demo@polystack.local', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Demo User');

INSERT INTO `tasks` (`id`, `user_id`, `title`, `prompt_body`, `description`, `is_reusable`) VALUES
  (1, 1, 'Summarize email', 'Summarize the following text in 3 bullet points:\n\n{{text}}', 'Reusable summarization prompt', 1),
  (2, 1, 'Code review', 'Review this code for bugs and style:\n\n{{code}}', NULL, 0);

INSERT INTO `executions` (`id`, `task_id`, `user_id`, `input_payload`, `output_payload`, `meta`) VALUES
  (1, 1, 1, '{"text":"Hello world. This is a test."}', '{"summary":["Point A","Point B","Point C"]}', JSON_OBJECT('model', 'demo'));

INSERT INTO `ratings` (`user_id`, `execution_id`, `score`, `comment`) VALUES
  (1, 1, 4, 'Good structure');

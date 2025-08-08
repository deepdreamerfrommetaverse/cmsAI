<?php
/**
 * Plugin Name: AI Article Generator and Integrator
 * Description: Generates a blog article with AI (text and image) and integrates with BricksBuilder and social media embeds.
 * Version: 1.0.1
 * Author: Your Name
 */

defined('ABSPATH') || exit;

// Define your OpenAI API key (replace 'sk-XXXX' with your actual key).
define('MY_OPENAI_API_KEY', 'sk-XXXX');  // Ustaw swój klucz API OpenAI tutaj.

// Add an admin menu page for the plugin.
add_action('admin_menu', 'myplugin_add_admin_menu');
function myplugin_add_admin_menu() {
    add_menu_page(
        'AI Article Generator',        // Tytuł strony
        'AI Article Generator',        // Tytuł w menu
        'manage_options',             // Wymagana rola
        'ai-article-generator',       // Unikalny identyfikator strony
        'myplugin_render_admin_page', // Funkcja wyświetlająca zawartość
        'dashicons-edit-page'         // Ikona w menu (ikonka edycji strony)
    );
}

// Render the admin page content and handle form submissions.
function myplugin_render_admin_page() {
    if (!current_user_can('manage_options')) {
        return;
    }

    $error_message = '';
    $success_message = '';
    if (isset($_POST['myplugin_generate_article'])) {
        // Check nonce for security
        if (!isset($_POST['myplugin_nonce']) || !wp_verify_nonce($_POST['myplugin_nonce'], 'myplugin_generate')) {
            $error_message = 'Błędny token zabezpieczający. Spróbuj ponownie.';
        } else {
            // Sanitize inputs
            $topic = sanitize_text_field($_POST['article_topic'] ?? '');
            $ig_url = esc_url_raw($_POST['instagram_url'] ?? '');
            $tw_url = esc_url_raw($_POST['twitter_url'] ?? '');

            if (empty($topic)) {
                $error_message = 'Podaj temat artykułu.';
            } else {
                // Generate the article (text, image, etc.)
                $result = myplugin_generate_article($topic, $ig_url, $tw_url);
                if (is_wp_error($result)) {
                    $error_message = 'Nie udało się wygenerować artykułu. ' . esc_html($result->get_error_message());
                } else {
                    $post_id = $result;
                    $edit_link = esc_url(get_edit_post_link($post_id));
                    $view_link = esc_url(get_permalink($post_id));
                    $success_message  = 'Artykuł został pomyślnie wygenerowany! ';
                    $success_message .= '<a href="'.$edit_link.'">Edytuj wpis</a> lub ';
                    $success_message .= '<a href="'.$view_link.'" target="_blank">Zobacz wpis</a>.';
                }
            }
        }
    }

    // Output the page form and any messages
    echo '<div class="wrap">';
    echo '<h1>Generator Artykułów AI</h1>';
    if ($error_message) {
        echo '<div class="notice notice-error"><p>' . $error_message . '</p></div>';
    }
    if ($success_message) {
        echo '<div class="notice notice-success"><p>' . $success_message . '</p></div>';
    }
    echo '<form method="post" action="">';
    wp_nonce_field('myplugin_generate', 'myplugin_nonce');
    echo '<table class="form-table"><tbody>';
    echo '<tr><th scope="row"><label for="article_topic">Temat artykułu</label></th>';
    echo '<td><input name="article_topic" type="text" id="article_topic" value="" class="regular-text" ';
    echo 'placeholder="Wprowadź temat lub krótki opis artykułu" required></td></tr>';
    echo '<tr><th scope="row"><label for="instagram_url">Post z Instagrama (opcjonalnie)</label></th>';
    echo '<td><input name="instagram_url" type="url" id="instagram_url" value="" class="regular-text" ';
    echo 'placeholder="URL do posta na Instagramie (opcjonalnie)"></td></tr>';
    echo '<tr><th scope="row"><label for="twitter_url">Post z Twittera (opcjonalnie)</label></th>';
    echo '<td><input name="twitter_url" type="url" id="twitter_url" value="" class="regular-text" ';
    echo 'placeholder="URL do posta na Twitterze (opcjonalnie)"></td></tr>';
    echo '</tbody></table>';
    echo '<p class="submit"><button type="submit" name="myplugin_generate_article" class="button button-primary">';
    echo 'Wygeneruj artykuł</button></p>';
    echo '</form>';
    echo '</div>';
}

/**
 * Generate the article content and create a new post.
 *
 * @param string $topic The topic or brief for the article.
 * @param string $ig_url (optional) Instagram post URL to embed.
 * @param string $twitter_url (optional) Twitter post URL to embed.
 * @return int|WP_Error Post ID on success, or WP_Error on failure.
 */
function myplugin_generate_article($topic, $ig_url = '', $twitter_url = '') {
    // Generate the article text using OpenAI
    $article_text = myplugin_generate_text($topic);
    if (is_wp_error($article_text)) {
        return $article_text;
    }
    // Generate an image for the article
    $image_url = myplugin_generate_image($topic);
    if (is_wp_error($image_url)) {
        return $image_url;
    }

    // Create the new post in draft status first
    $post_title = wp_trim_words($topic, 12, '');
    if (empty($post_title)) {
        $post_title = 'Nowy artykuł';
    }
    $post_id = wp_insert_post(array(
        'post_title'   => $post_title,
        'post_content' => '',
        'post_status'  => 'draft',
        'post_author'  => get_current_user_id()
    ));
    if (is_wp_error($post_id) || $post_id == 0) {
        return new WP_Error('post_error', 'Błąd podczas tworzenia wpisu.');
    }

    // If an image URL was returned, sideload it and attach to post
    $attach_id = 0;
    if (!empty($image_url)) {
        require_once(ABSPATH . 'wp-admin/includes/media.php');
        require_once(ABSPATH . 'wp-admin/includes/file.php');
        require_once(ABSPATH . 'wp-admin/includes/image.php');
        $attach_id = media_sideload_image($image_url, $post_id, $post_title, 'id');
        if (is_wp_error($attach_id)) {
            wp_delete_post($post_id, true);
            return new WP_Error('image_error', 'Nie udało się dodać obrazu do artykułu.');
        } else {
            // Set featured image
            set_post_thumbnail($post_id, $attach_id);
        }
    }

    // Build final content
    $final_content = $article_text;
    if ($attach_id) {
        $image_src = wp_get_attachment_url($attach_id);
        if ($image_src) {
            $final_content .= "\n\n" . '<p><img src="' . esc_url($image_src) . '" alt="' . esc_attr($post_title) . '" /></p>';
        }
    }
    if (!empty($ig_url)) {
        $final_content .= "\n\n" . '<p><strong>Źródło (Instagram):</strong></p>';
        $final_content .= '<blockquote class="instagram-media" data-instgrm-permalink="' . esc_url($ig_url) . '" data-instgrm-version="14"></blockquote>';
        $final_content .= '<script async src="//www.instagram.com/embed.js"></script>';
    }
    if (!empty($twitter_url)) {
        $final_content .= "\n\n" . '<p><strong>Źródło (Twitter):</strong></p>';
        $final_content .= '<blockquote class="twitter-tweet"><a href="' . esc_url($twitter_url) . '"></a></blockquote>';
        $final_content .= '<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>';
    }

    // Update post content and publish
    wp_update_post(array(
        'ID'           => $post_id,
        'post_content' => $final_content,
        'post_status'  => 'publish'
    ));
    return $post_id;
}

/**
 * Call OpenAI's API to generate article text based on a topic.
 */
function myplugin_generate_text($topic) {
    $prompt = "Napisz artykuł na temat: \"{$topic}\".\n\nArtykuł powinien być szczegółowy, z podziałem na akapity i nagłówki, oraz ciekawy dla czytelnika.";
    $api_url = 'https://api.openai.com/v1/chat/completions';
    $request_body = array(
        'model' => 'gpt-3.5-turbo',
        'messages' => array(
            array('role' => 'system', 'content' => 'Jesteś pomocnym asystentem, który pisze artykuły blogowe.'),
            array('role' => 'user', 'content' => $prompt)
        ),
        'temperature' => 0.7,
        'max_tokens' => 1000
    );
    $args = array(
        'headers' => array(
            'Content-Type' => 'application/json',
            'Authorization' => 'Bearer ' . MY_OPENAI_API_KEY
        ),
        'body' => json_encode($request_body),
        'timeout' => 60
    );
    $response = wp_remote_post($api_url, $args);
    if (is_wp_error($response)) {
        return new WP_Error('openai_request_failed', 'Błąd połączenia z API OpenAI.');
    }
    $response_code = wp_remote_retrieve_response_code($response);
    if ($response_code !== 200) {
        $body = wp_remote_retrieve_body($response);
        $data = json_decode($body, true);
        $msg = isset($data['error']['message']) ? $data['error']['message'] : 'Nieznany błąd API.';
        return new WP_Error('openai_api_error', 'OpenAI: ' . $msg);
    }
    $body = wp_remote_retrieve_body($response);
    $data = json_decode($body, true);
    if (empty($data['choices'][0]['message']['content'])) {
        return new WP_Error('openai_no_content', 'OpenAI nie zwrócił treści artykułu.');
    }
    $article_text = $data['choices'][0]['message']['content'];
    // Sanitize output (allow basic formatting tags)
    $article_text = wp_kses_post($article_text);
    return $article_text;
}

/**
 * Call OpenAI's Image Generation API (DALL-E) to get an image URL for the topic.
 */
function myplugin_generate_image($topic) {
    // Use the topic as prompt for image generation (assuming it describes what to illustrate)
    $prompt = $topic;
    $api_url = 'https://api.openai.com/v1/images/generations';
    $request_body = array(
        'prompt' => $prompt,
        'n' => 1,
        'size' => '1024x1024'
    );
    $args = array(
        'headers' => array(
            'Content-Type' => 'application/json',
            'Authorization' => 'Bearer ' . MY_OPENAI_API_KEY
        ),
        'body' => json_encode($request_body),
        'timeout' => 60
    );
    $response = wp_remote_post($api_url, $args);
    if (is_wp_error($response)) {
        return new WP_Error('openai_image_failed', 'Błąd połączenia przy generowaniu obrazu.');
    }
    $response_code = wp_remote_retrieve_response_code($response);
    if ($response_code !== 200) {
        $body = wp_remote_retrieve_body($response);
        $data = json_decode($body, true);
        $msg = isset($data['error']['message']) ? $data['error']['message'] : 'Nieznany błąd generowania obrazu.';
        return new WP_Error('openai_image_error', 'OpenAI (Obraz): ' . $msg);
    }
    $body = wp_remote_retrieve_body($response);
    $data = json_decode($body, true);
    if (empty($data['data'][0]['url'])) {
        return new WP_Error('openai_image_no_url', 'Nie otrzymano URL wygenerowanego obrazu.');
    }
    return $data['data'][0]['url'];
}

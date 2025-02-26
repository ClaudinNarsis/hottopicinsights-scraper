// Utility functions
const parseTraffic = (trafficStr) => {
    console.log('Parsing traffic string:', trafficStr);
    if (!trafficStr) return 'N/A';
    // Keep the original traffic string format (e.g., "100+", "5000+")
    return trafficStr;
};

const isEnglish = (text) => {
    console.log('Checking if text is English:', text);
    // Simple check for ASCII characters
    return /^[\x00-\x7F]*$/.test(text);
};

// Main function to fetch trends
async function fetchTrends(geo = 'IN') {
    console.log('Starting fetchTrends with geo:', geo);
    try {
        // Using a CORS proxy to access Google Trends RSS feed
        const proxyUrl = 'https://api.allorigins.win/raw?url=';
        const url = `${proxyUrl}${encodeURIComponent(`https://trends.google.com/trending/rss?geo=${geo}&hours=24&status=active&hl=en-US`)}`;
        console.log('Fetching from URL:', url);
        
        const response = await fetch(url);
        console.log('Response status:', response.status);
        if (!response.ok) throw new Error('Network response was not ok');
        
        const text = await response.text();
        console.log('Received XML length:', text.length);
        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(text, 'text/xml');
        
        // Process items
        const items = xmlDoc.getElementsByTagName('item');
        console.log('Found number of items:', items.length);
        let trends = [];
        
        for (const item of items) {
            const title = item.getElementsByTagName('title')[0].textContent;
            console.log('Processing trend:', title);
            if (!isEnglish(title)) {
                console.log('Skipping non-English trend:', title);
                continue;
            }
            
            // Get traffic and picture using getElementsByTagName
            const trafficElements = item.getElementsByTagName('ht:approx_traffic');
            const pictureElements = item.getElementsByTagName('ht:picture');
            
            const traffic = trafficElements.length > 0 ? trafficElements[0].textContent : 'N/A';
            const picture = pictureElements.length > 0 ? pictureElements[0].textContent : null;
            
            console.log('Trend traffic:', traffic, 'Picture:', picture ? 'Yes' : 'No');
            
            // Get news items using getElementsByTagName
            const newsItemElements = item.getElementsByTagName('ht:news_item');
            const newsItems = Array.from(newsItemElements).map(news => {
                const titleElements = news.getElementsByTagName('ht:news_item_title');
                const sourceElements = news.getElementsByTagName('ht:news_item_source');
                const urlElements = news.getElementsByTagName('ht:news_item_url');
                const pictureElements = news.getElementsByTagName('ht:news_item_picture');
                
                const newsItem = {
                    title: titleElements.length > 0 ? titleElements[0].textContent : '',
                    source: sourceElements.length > 0 ? sourceElements[0].textContent : '',
                    url: urlElements.length > 0 ? urlElements[0].textContent : '',
                    news_item_picture: pictureElements.length > 0 ? pictureElements[0].textContent : null
                };
                console.log('Parsed news item:', newsItem.title);
                return newsItem;
            });
            
            console.log('Number of news items for trend:', newsItems.length);
            
            trends.push({
                topic: title,
                traffic,
                picture,
                news_items: newsItems
            });
        }
        
        // Sort trends by traffic (highest to lowest)
        trends.sort((a, b) => {
            const getNumericTraffic = (str) => parseInt(str.replace(/[^0-9]/g, '')) || 0;
            return getNumericTraffic(b.traffic) - getNumericTraffic(a.traffic);
        });
        
        console.log('Sorted trends count:', trends.length);
        console.log('Final trends count:', trends.length);
        
        return trends;
    } catch (error) {
        console.error('Error fetching trends:', error);
        return [];
    }
}

// Function to generate the main HTML content
function generateMainHTML(trends) {
    console.log('Starting to generate main HTML with trends:', trends.length);
    const mainContent = document.createElement('div');
    mainContent.className = 'container';
    
    const logo = document.createElement('img');
    logo.src = 'src/logo.png';
    logo.alt = 'Hot Topic Insights Logo';
    logo.className = 'logo';
    mainContent.appendChild(logo);
    console.log('Added logo to main content');
    
    const heading = document.createElement('h1');
    heading.innerHTML = '<span class="brand">Hot Topic Insights</span> - Trending Now';
    mainContent.appendChild(heading);
    
    const trendsGrid = document.createElement('div');
    trendsGrid.className = 'trends-grid';
    
    trends.forEach((trend, index) => {
        console.log(`Processing trend ${index + 1}/${trends.length}:`, trend.topic);
        const mainHeadline = trend.news_items[0]?.title || trend.topic;
        const trendImage = trend.picture || (trend.news_items[0]?.news_item_picture);
        const encodedTopic = encodeURIComponent(trend.topic.toLowerCase());
        
        const trendElement = document.createElement('a');
        trendElement.href = `index.html?topic=${encodedTopic}`;
        trendElement.className = 'trend';
        
        let trendHTML = '';
        if (trendImage) {
            trendHTML += `<img src="${trendImage}" alt="${trend.topic}" class="trend-image">`;
            console.log('Added image for trend:', trend.topic);
        }
        
        trendHTML += `
            <div class="trend-content">
                <div class="trend-topic">${trend.topic}</div>
                <h2>
                    ${mainHeadline}
                    <span class="traffic">${trend.traffic} searches</span>
                </h2>
                <div class="news-items">
        `;
        
        if (trend.news_items.length > 0) {
            const firstNews = trend.news_items[0];
            trendHTML += `
                <div class="news-item">
                    <div class="source">Source: ${firstNews.source}</div>
                </div>
            `;
        }
        
        trendHTML += `
                </div>
            </div>
        `;
        
        trendElement.innerHTML = trendHTML;
        trendsGrid.appendChild(trendElement);
    });
    
    mainContent.appendChild(trendsGrid);
    console.log('Completed generating main HTML');
    return mainContent;
}

// Function to generate story HTML
function generateStoryHTML(trend) {
    const storyContent = document.createElement('div');
    storyContent.className = 'container story-page';
    
    // Add back button
    const backButton = document.createElement('a');
    backButton.href = './index.html';
    backButton.className = 'back-button';
    backButton.innerHTML = '&larr; Back to Trends';
    storyContent.appendChild(backButton);
    
    let html = `
        <h1>Hot Topic Insights: ${trend.topic}</h1>
        <div class="traffic">Trending with ${trend.traffic}</div>
    `;
    
    if (trend.picture) {
        html += `<img class="cover-image" src="${trend.picture}" alt="Cover image for ${trend.topic}">`;
    }
    
    if (trend.news_items && trend.news_items.length > 0) {
        html += '<div class="news-items">';
        trend.news_items.forEach(news => {
            if (news.title && news.source) {  // Only show news items with valid title and source
                html += `
                    <div class="news-item">
                        ${news.news_item_picture ? `<img class="news-image" src="${news.news_item_picture}" alt="${news.title}">` : ''}
                        <div class="news-content">
                            <h2>${news.title}</h2>
                            <p class="news-source">Source: ${news.source}</p>
                            <a href="${news.url}" target="_blank" class="read-more">
                                Read more <i class="fas fa-external-link-alt"></i>
                            </a>
                        </div>
                    </div>
                `;
            }
        });
        html += '</div>';
    } else {
        html += '<p class="no-news">No additional news items available for this trend.</p>';
    }
    
    html += `
        <div class="footer">
            <p>&copy; ${new Date().getFullYear()} <span class="brand">Hot Topic Insights</span>. All rights reserved.</p>
        </div>
    `;
    
    storyContent.innerHTML += html;
    return storyContent;
}

// Initialize the application
async function initApp() {
    console.log('Starting application initialization');
    try {
        const trends = await fetchTrends();
        console.log('Successfully fetched trends:', trends.length);
        
        // Check if we're on a story page
        const urlParams = new URLSearchParams(window.location.search);
        const storyTopic = urlParams.get('topic');
        
        if (storyTopic) {
            // Find the matching trend
            const trend = trends.find(t => t.topic.toLowerCase() === decodeURIComponent(storyTopic).toLowerCase());
            if (trend) {
                const storyContent = generateStoryHTML(trend);
                document.body.innerHTML = '';
                document.body.appendChild(storyContent);
                console.log('Displayed story page for:', trend.topic);
            } else {
                console.error('Story not found:', storyTopic);
                window.location.href = './index.html'; // Redirect to home if story not found
            }
        } else {
            // Generate and display main page content
            const mainContent = generateMainHTML(trends);
            console.log('Generated main HTML content');
            
            document.body.innerHTML = '';
            document.body.appendChild(mainContent);
            console.log('Added main content to document body');
        }
        
        console.log('Application initialization completed');
    } catch (error) {
        console.error('Error during app initialization:', error);
    }
}

// Start the application when the page loads
window.addEventListener('load', () => {
    console.log('Page loaded, starting application');
    initApp();
}); 
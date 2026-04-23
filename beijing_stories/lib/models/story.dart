class Story {
  final String id;
  final String title;
  final String subtitle;
  final String location;
  final String region;
  final String era;
  final String type;
  final String coverImage;
  final List<String> images;
  final String? audioUrl;
  final String introduction;
  final String content;
  final String address;
  final String? openingHours;
  final String? ticketPrice;
  final List<String> relatedStoryIds;
  final int viewCount;

  Story({
    required this.id,
    required this.title,
    required this.subtitle,
    required this.location,
    required this.region,
    required this.era,
    required this.type,
    required this.coverImage,
    required this.images,
    this.audioUrl,
    required this.introduction,
    required this.content,
    required this.address,
    this.openingHours,
    this.ticketPrice,
    required this.relatedStoryIds,
    this.viewCount = 0,
  });

  factory Story.fromJson(Map<String, dynamic> json) {
    return Story(
      id: json['id'] as String,
      title: json['title'] as String,
      subtitle: json['subtitle'] as String,
      location: json['location'] as String,
      region: json['region'] as String,
      era: json['era'] as String,
      type: json['type'] as String,
      coverImage: json['coverImage'] as String,
      images: List<String>.from(json['images'] as List),
      audioUrl: json['audioUrl'] as String?,
      introduction: json['introduction'] as String,
      content: json['content'] as String,
      address: json['address'] as String,
      openingHours: json['openingHours'] as String?,
      ticketPrice: json['ticketPrice'] as String?,
      relatedStoryIds: List<String>.from(json['relatedStoryIds'] as List),
      viewCount: json['viewCount'] as int? ?? 0,
    );
  }
}

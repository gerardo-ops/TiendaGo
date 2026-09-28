using System;
using System.Collections.Generic;

namespace TiendaGo.Models;

public partial class S3MultipartUploads
{
    public string Id { get; set; } = null!;

    public long InProgressSize { get; set; }

    public string UploadSignature { get; set; } = null!;

    public string BucketId { get; set; } = null!;

    public string Key { get; set; } = null!;

    public string Version { get; set; } = null!;

    public string? OwnerId { get; set; }

    public DateTime CreatedAt { get; set; }

    public string? UserMetadata { get; set; }

    public string? Metadata { get; set; }

    public virtual Buckets Bucket { get; set; } = null!;

    public virtual ICollection<S3MultipartUploadsParts> S3MultipartUploadsParts { get; set; } = new List<S3MultipartUploadsParts>();
}
